"""YouTube Analytics API v2 — métricas de performance por vídeo e intervalo.

Nada de métrica não documentada é assumida. Se a API rejeitar um identificador
(``engagedViews``, filtro ``creatorContentType==SHORTS`` em contas que não
suportam), ele é removido e a coleta segue, marcando o campo como indisponível.

Limitação conhecida e **sem** contorno: a métrica visual do YouTube Studio
"continuaram assistindo / deslizaram para fora" (swipe-away dos Shorts) não é
exposta por nenhuma API pública. Não há scraping. Ela fica fora deste módulo.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from youtube.client import YouTubeClient  # noqa: E402
from youtube.errors import MetricUnavailableError, YouTubeError  # noqa: E402
from youtube.log import E_COLLECT_ANALYTICS, get_logger  # noqa: E402
from youtube.util import iso, parse_rfc3339, utcnow  # noqa: E402

log = get_logger("youtube.analytics")

# Ordem estável; engagedViews é opcional e cai fora se a conta não expõe.
CORE_METRICS = [
    "views", "estimatedMinutesWatched", "averageViewDuration",
    "averageViewPercentage", "likes", "comments", "shares",
    "subscribersGained", "subscribersLost",
]
OPTIONAL_METRICS = ["engagedViews"]

_UNKNOWN_METRIC_RE = re.compile(r"metric[s]?[^\w]+([a-zA-Z]+)")
_UNKNOWN_FILTER_RE = re.compile(r"(creatorContentType|filter)")


def _date(d, fallback):
    if d is None:
        return fallback
    if hasattr(d, "strftime"):
        return d.strftime("%Y-%m-%d")
    return str(d)[:10]


def query_video(client: YouTubeClient, video_id: str, *, start_date=None, end_date=None,
                shorts_only: bool = False, channel_id: str | None = None) -> dict:
    """Métricas agregadas de um vídeo no intervalo [start_date, end_date].

    Datas em ``YYYY-MM-DD`` ou ``date``. Default: 2005-02-14 (nascimento do
    YouTube) até hoje — ou seja, acumulado de vida.
    """
    ids = f"channel=={channel_id}" if channel_id else "channel==MINE"
    end = _date(end_date, utcnow().strftime("%Y-%m-%d"))
    start = _date(start_date, "2005-02-14")
    metrics = CORE_METRICS + OPTIONAL_METRICS
    drop: set[str] = set()
    use_shorts_filter = shorts_only

    for _ in range(4):
        flt = f"video=={video_id}"
        if use_shorts_filter:
            flt += ";creatorContentType==SHORTS"
        active = [m for m in metrics if m not in drop]
        try:
            resp = client.execute(client.analytics.reports().query(
                ids=ids, startDate=start, endDate=end,
                metrics=",".join(active), filters=flt))
            break
        except YouTubeError as exc:
            msg = str(exc)
            m = _UNKNOWN_METRIC_RE.search(msg)
            if m and m.group(1) in metrics and m.group(1) not in drop:
                drop.add(m.group(1))
                log.warning("%s metrica indisponivel: %s", E_COLLECT_ANALYTICS, m.group(1))
                continue
            if use_shorts_filter and _UNKNOWN_FILTER_RE.search(msg):
                use_shorts_filter = False
                log.warning("%s filtro creatorContentType==SHORTS nao suportado; ignorando", E_COLLECT_ANALYTICS)
                continue
            raise
    else:
        raise MetricUnavailableError(f"Analytics não respondeu para {video_id}.")

    cols = [h["name"] for h in resp.get("columnHeaders", [])]
    rows = resp.get("rows") or [[None] * len(cols)]
    values = dict(zip(cols, rows[0]))
    out = {
        "period_start": start, "period_end": end,
        "creator_content_type": "SHORTS" if use_shorts_filter else None,
        "metrics": {k: _num(values.get(k)) for k in CORE_METRICS},
        "unavailable_metrics": sorted(drop),
    }
    out["metrics"]["engagedViews"] = _num(values.get("engagedViews")) if "engagedViews" not in drop else None
    log.info("%s video=%s intervalo=%s..%s", E_COLLECT_ANALYTICS, video_id, start, end)
    return out


def query_traffic_sources(client: YouTubeClient, video_id: str, *, start_date=None,
                          end_date=None, channel_id: str | None = None) -> dict:
    """{sourceType: views} — opcional, para a coluna traffic_source."""
    ids = f"channel=={channel_id}" if channel_id else "channel==MINE"
    end = _date(end_date, utcnow().strftime("%Y-%m-%d"))
    start = _date(start_date, "2005-02-14")
    try:
        resp = client.execute(client.analytics.reports().query(
            ids=ids, startDate=start, endDate=end, metrics="views",
            dimensions="insightTrafficSourceType", filters=f"video=={video_id}",
            sort="-views"))
    except YouTubeError:
        return {}
    return {r[0]: _num(r[1]) for r in resp.get("rows", [])}


def _num(v):
    if v is None:
        return None
    try:
        f = float(v)
        return int(f) if f.is_integer() else f
    except (TypeError, ValueError):
        return None


if __name__ == "__main__":
    import json
    c = YouTubeClient()
    vid = sys.argv[1]
    print(json.dumps(query_video(c, vid, shorts_only=True), indent=2, ensure_ascii=False))
    print("traffic:", query_traffic_sources(c, vid))
