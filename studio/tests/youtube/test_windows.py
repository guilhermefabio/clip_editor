from youtube import windows


def test_classify_due_missed_pending():
    # vídeo com ~24h de idade, nada capturado
    r = windows.classify(24.0, captured=set())
    assert "24h" in r["due"]
    assert "1h" in r["missed"] and "6h" in r["missed"]
    assert "72h" in r["pending"] and "7d" in r["pending"]


def test_classify_skips_captured():
    r = windows.classify(24.0, captured={"1h", "6h", "24h"})
    assert r["due"] == []
    assert r["missed"] == []


def test_classify_none_age():
    r = windows.classify(None, set())
    assert r["due"] == [] and r["missed"] == []
    assert set(r["pending"]) == set(windows.cfg.AGE_WINDOWS_HOURS)


def test_window_date_range_clamps_to_today():
    start, end = windows.window_date_range("2026-09-05T12:00:00Z", "1h")
    assert start == "2026-09-05"
    assert end >= start


def test_next_check_hint():
    assert windows.next_check_hint(0.1) == "1h"
    assert windows.next_check_hint(2) == "6h"
    assert windows.next_check_hint(10_000) is None
