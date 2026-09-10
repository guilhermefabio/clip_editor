"""Fixtures do módulo youtube — tudo local, sem tocar na API real."""
import sys
from pathlib import Path

import pytest

STUDIO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(STUDIO))

from youtube import storage  # noqa: E402


@pytest.fixture
def db(tmp_path):
    conn = storage.connect(tmp_path / "t.db")
    storage.init_db(conn)
    yield conn
    conn.close()


@pytest.fixture
def fake_video():
    return {
        "video_id": "vid123",
        "title": "FLANCO PELA LATERAL",
        "published_at": "2026-09-05T12:00:00Z",
        "channel_id": "chan1",
        "duration_seconds": 21.0,
        "is_short": True,
        "view_count": 1000,
        "like_count": 80,
        "comment_count": 12,
    }


@pytest.fixture
def analytics_rows():
    """Resposta típica da Analytics API (reports.query)."""
    return {
        "columnHeaders": [
            {"name": "views"}, {"name": "estimatedMinutesWatched"},
            {"name": "averageViewDuration"}, {"name": "averageViewPercentage"},
            {"name": "likes"}, {"name": "comments"}, {"name": "shares"},
            {"name": "subscribersGained"}, {"name": "subscribersLost"},
            {"name": "engagedViews"},
        ],
        "rows": [[1300, 300.0, 13.8, 62.5, 90, 10, 6, 22, 3, 900]],
    }


class FakeRequest:
    def __init__(self, result): self._r = result
    def execute(self): return self._r


class FakeReports:
    def __init__(self, result, on_query=None):
        self._r, self._on_query = result, on_query
    def query(self, **kwargs):
        if self._on_query:
            self._on_query(kwargs)
        return FakeRequest(self._r)


class FakeClient:
    """Só o suficiente para analytics_api/collector."""
    def __init__(self, analytics_result=None, on_query=None):
        self.analytics = type("A", (), {"reports": lambda self_: FakeReports(analytics_result or {}, on_query)})()
        self.data = None
    def execute(self, request, **kw):
        return request.execute()


@pytest.fixture
def fake_client(analytics_rows):
    return FakeClient(analytics_rows)
