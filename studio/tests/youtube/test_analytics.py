"""Parsing da Analytics API sem rede."""
import pytest
from youtube import analytics_api
from youtube.errors import YouTubeError


class _Req:
    def __init__(self, results):
        self._results = list(results)     # cada item: dict OU Exception
    def execute(self):
        r = self._results.pop(0)
        if isinstance(r, Exception):
            raise r
        return r


class _Reports:
    def __init__(self, results):
        self._req = _Req(results)
    def query(self, **kw):
        self._kw = kw
        return self._req


class _Client:
    def __init__(self, results):
        self.analytics = type("A", (), {"reports": lambda s: self._reports})()
        self._reports = _Reports(results)
    def execute(self, request, **kw):
        return request.execute()


FULL = {
    "columnHeaders": [{"name": n} for n in
        ["views", "estimatedMinutesWatched", "averageViewDuration",
         "averageViewPercentage", "likes", "comments", "shares",
         "subscribersGained", "subscribersLost", "engagedViews"]],
    "rows": [[1300, 300.0, 13.8, 62.5, 90, 10, 6, 22, 3, 900]],
}


def test_query_video_maps_metrics():
    c = _Client([FULL])
    out = analytics_api.query_video(c, "vid", start_date="2026-09-05", end_date="2026-09-06")
    m = out["metrics"]
    assert m["views"] == 1300 and m["likes"] == 90 and m["engagedViews"] == 900
    assert out["period_start"] == "2026-09-05"
    assert out["unavailable_metrics"] == []


def test_query_video_incomplete_response():
    c = _Client([{"columnHeaders": [{"name": "views"}], "rows": []}])
    out = analytics_api.query_video(c, "vid")
    assert out["metrics"]["views"] is None
    assert out["metrics"]["likes"] is None            # coluna ausente -> None, sem crash


def test_query_video_drops_unknown_metric_then_succeeds():
    err = YouTubeError("Erro da API (400/badRequest). unknown metric engagedViews")
    ok = {k: v for k, v in FULL.items()}
    ok = {"columnHeaders": FULL["columnHeaders"][:-1], "rows": [[r for r in FULL["rows"][0][:-1]]]}
    c = _Client([err, ok])
    out = analytics_api.query_video(c, "vid")
    assert "engagedViews" in out["unavailable_metrics"]
    assert out["metrics"]["engagedViews"] is None
    assert out["metrics"]["views"] == 1300


def test_query_video_raises_when_never_succeeds():
    errs = [YouTubeError("Erro da API (500/backendError).")] * 5
    with pytest.raises(YouTubeError):
        analytics_api.query_video(_Client(errs), "vid")
