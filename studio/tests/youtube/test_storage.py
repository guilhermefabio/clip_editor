from youtube import storage


def test_upsert_video_idempotent(db, fake_video):
    storage.upsert_video(db, fake_video)
    storage.upsert_video(db, {**fake_video, "title": "NOVO TITULO"})
    rows = storage.all_videos(db)
    assert len(rows) == 1
    assert rows[0]["title"] == "NOVO TITULO"
    assert rows[0]["is_short"] == 1


def test_snapshots_are_append_only(db, fake_video):
    storage.upsert_video(db, fake_video)
    base = {"video_id": "vid123", "captured_at": "2026-09-06T12:00:00Z",
            "video_age_hours": 24, "age_window": "24h", "views": 800}
    storage.insert_snapshot(db, base)
    storage.insert_snapshot(db, {**base, "captured_at": "2026-09-08T12:00:00Z",
                                 "age_window": "72h", "views": 1350})
    snaps = storage.snapshots_for(db, "vid123")
    assert [s["views"] for s in snaps] == [800, 1350]           # ordem por captured_at
    assert storage.snapshot_exists(db, "vid123", "24h")
    assert not storage.snapshot_exists(db, "vid123", "7d")
    assert storage.latest_snapshot(db, "vid123")["views"] == 1350
    assert storage.latest_snapshot(db, "vid123", "24h")["views"] == 800


def test_snapshot_serialises_json_and_csv(db):
    sid = storage.insert_snapshot(db, {
        "video_id": "v", "captured_at": "2026-09-06T00:00:00Z",
        "derived_json": {"engaged_view_rate": 0.69},
        "quality_json": {"quality_score": 0.5},
        "unavailable_metrics": ["engagedViews"],
    })
    row = storage.snapshots_for(db, "v")[0]
    assert sid > 0
    assert '"engaged_view_rate": 0.69' in row["derived_json"]
    assert row["unavailable_metrics"] == "engagedViews"


def test_links(db):
    storage.set_link(db, "shorts_bodycam_lote15/70_X", "vidABC", "title", 0.87)
    storage.set_link(db, "shorts_bodycam_lote15/70_X", "vidABC", "manual", 1.0)  # upsert
    links = storage.all_links(db)
    assert links["shorts_bodycam_lote15/70_X"]["video_id"] == "vidABC"
    assert links["shorts_bodycam_lote15/70_X"]["matched_by"] == "manual"
