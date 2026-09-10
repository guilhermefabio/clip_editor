"""Funções puras e sem dependência de rede (fáceis de testar)."""
from __future__ import annotations

import re
from datetime import datetime, timezone

_ISO_DUR = re.compile(
    r"^P(?:(?P<days>\d+)D)?"
    r"(?:T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+(?:\.\d+)?)S)?)?$"
)


def parse_iso8601_duration(text: str | None) -> float:
    """``PT1M30S`` -> ``90.0`` segundos. Aceita dias e frações de segundo.

    Retorna 0.0 para entrada vazia; ``ValueError`` para formato inválido.
    """
    if not text:
        return 0.0
    m = _ISO_DUR.match(text.strip())
    if not m:
        raise ValueError(f"Duração ISO 8601 inválida: {text!r}")
    p = m.groupdict()
    return (
        int(p["days"] or 0) * 86400
        + int(p["hours"] or 0) * 3600
        + int(p["minutes"] or 0) * 60
        + float(p["seconds"] or 0.0)
    )


def parse_rfc3339(text: str | None) -> datetime | None:
    """``2026-09-07T15:00:47Z`` -> datetime tz-aware (UTC)."""
    if not text:
        return None
    t = text.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(t)
    except ValueError:
        return None
    return dt.astimezone(timezone.utc) if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def age_hours(published_at: str | datetime | None, *, now: datetime | None = None) -> float | None:
    pub = parse_rfc3339(published_at) if isinstance(published_at, str) else published_at
    if pub is None:
        return None
    return round(((now or utcnow()) - pub).total_seconds() / 3600.0, 3)


def chunked(seq, n):
    seq = list(seq)
    for i in range(0, len(seq), n):
        yield seq[i:i + n]
