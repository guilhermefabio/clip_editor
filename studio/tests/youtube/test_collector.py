"""Collector com Data/Analytics mockados."""
import pytest
from youtube import collector, storage


@pytest.fixture
def patched(monkeypatch, fake_video):
    monkeypatch.setattr(collector.data_api, "get_video", lambda client, vid: {**fake_video, "video_id": vid})
    monkeypatch.setattr(collector.analytics_api, "query_video", lambda *a, **k: {
        "period_start": "2026-09-05", "period_end": "2026-09-06",
        "creator_content_type": None, "unavailable_metrics": [],
        "metrics": {"views": 1300, "likes": 90, "comments": 10, "shares": 6,
                    "subscribersGained": 22, "subscribersLost": 3, "engagedViews": 900,
                    "averageViewPercentage": 62.5, "estimatedMinutesWatched": 300.0,
                    "averageViewDuration": 13.8},
    })
    monkeypatch.setattr(collector.analytics_api, "query_traffic_sources", lambda *a, **k: {"SHORTS": 1200, "BROWSE": 100})
    monkeypatch.setattr(collector.versions, "stamp", lambda: {
        "editor_version": "0.1.0+aaa", "detector_version": "0.1.0+bbb",
        "ranking_model_version": "0.1.0+ccc", "render_config_version": "0.1.0+ddd"})


def test_collect_metrics_writes_snapshot(db, patched):
    snap = collector.collect_metrics_for_video("vidX", "2026-09-05", "2026-09-06",
                                               age_window="24h", conn=db, client=object())
    assert snap["views"] == 1300
    assert snap["traffic_source"] == "SHORTS"
    assert snap["editor_version"] == "0.1.0+aaa"
    stored = storage.snapshots_for(db, "vidX")
    assert len(stored) == 1
    import json
    assert json.loads(stored[0]["derived_json"])["engaged_view_rate"] == 900 / 1300


def test_window_snapshot_is_idempotent(db, patched):
    a = collector.collect_metrics_for_video("vidX", age_window="24h", conn=db, client=object())
    b = collector.collect_metrics_for_video("vidX", age_window="24h", conn=db, client=object())
    assert a is not None and b is None
    assert len(storage.snapshots_for(db, "vidX")) == 1
    c = collector.collect_metrics_for_video("vidX", age_window="24h", conn=db, client=object(), force=True)
    assert c is not None
    assert len(storage.snapshots_for(db, "vidX")) == 2


def test_adhoc_snapshot_always_appends(db, patched):
    collector.collect_metrics_for_video("vidX", conn=db, client=object())
    collector.collect_metrics_for_video("vidX", conn=db, client=object())
    assert len(storage.snapshots_for(db, "vidX")) == 2


def test_one_bad_video_does_not_stop_channel(db, patched, monkeypatch, fake_video):
    storage.upsert_video(db, {**fake_video, "video_id": "good1"})
    storage.upsert_video(db, {**fake_video, "video_id": "bad1"})
    monkeypatch.setattr(collector, "collect_channel", lambda *a, **k: None)

    def flaky(video, conn=None, client=None, *, force=False):
        if video["video_id"] == "bad1":
            raise RuntimeError("boom")
        return [{"video_id": "good1"}]

    monkeypatch.setattr(collector, "snapshot_due_windows", flaky)
    out = collector.collect_all_recent_videos(conn=db, client=object(), days=3650)
    assert out["snapshots"] == 1
    assert [e["video_id"] for e in out["errors"]] == ["bad1"]


def test_quota_stops_channel(db, patched, monkeypatch, fake_video):
    from youtube.errors import QuotaError
    storage.upsert_video(db, {**fake_video, "video_id": "v1"})
    monkeypatch.setattr(collector, "collect_channel", lambda *a, **k: None)
    monkeypatch.setattr(collector, "snapshot_due_windows",
                        lambda *a, **k: (_ for _ in ()).throw(QuotaError("cota")))
    out = collector.collect_all_recent_videos(conn=db, client=object(), days=3650)
    assert out.get("stopped") == "quota"
