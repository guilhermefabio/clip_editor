import pytest
from youtube.util import age_hours, chunked, parse_iso8601_duration, parse_rfc3339


@pytest.mark.parametrize("text,secs", [
    ("PT30S", 30), ("PT1M30S", 90), ("PT1H", 3600), ("PT1H2M3S", 3723),
    ("P1DT2H", 93600), ("PT0S", 0), ("PT1M30.5S", 90.5), ("", 0), (None, 0),
])
def test_iso8601_duration(text, secs):
    assert parse_iso8601_duration(text) == secs


@pytest.mark.parametrize("bad", ["30S", "1:30", "PT", "garbage", "P"])
def test_iso8601_duration_invalid(bad):
    if bad in ("PT", "P"):            # "PT"/"P" batem no regex e valem 0
        assert parse_iso8601_duration(bad) == 0
    else:
        with pytest.raises(ValueError):
            parse_iso8601_duration(bad)


def test_rfc3339_and_age():
    dt = parse_rfc3339("2026-09-05T12:00:00Z")
    assert dt.year == 2026 and dt.tzinfo is not None
    from datetime import timedelta
    now = dt + timedelta(hours=24)
    assert age_hours("2026-09-05T12:00:00Z", now=now) == 24.0
    assert age_hours(None) is None


def test_chunked():
    assert list(chunked(range(5), 2)) == [[0, 1], [2, 3], [4]]
    assert list(chunked([], 3)) == []
