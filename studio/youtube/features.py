"""Métricas derivadas e quality_score — SEM lógica de API aqui.

Separação proposital:
* *raw metrics*  -> vêm da Analytics API (views, likes, subscribersGained…);
* *derived metrics* -> só razões e taxas calculadas aqui;
* *quality_score* -> combinação **configurável e experimental** de componentes
  normalizados. Views absolutas de propósito não entram como sinal isolado.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from youtube import config as cfg  # noqa: E402

# Caps de normalização dos componentes do quality_score (0..1 após dividir).
ENGAGEMENT_CAP = 0.20      # (likes+comments+shares)/views ~ 20% já é altíssimo
SUBS_PER_1000_CAP = 20.0   # 20 inscritos por 1000 views ~ teto prático


def _rate(numerator, denominator, scale: float = 1.0):
    """Divisão segura: None se faltar dado ou denominador <= 0."""
    if numerator is None or denominator in (None, 0) or denominator < 0:
        return None
    return numerator / denominator * scale


def derived_metrics(raw: dict) -> dict:
    """raw = dict com chaves da Analytics (views, likes, engagedViews, …)."""
    views = raw.get("views")
    likes = raw.get("likes")
    comments = raw.get("comments")
    shares = raw.get("shares")
    gained = raw.get("subscribersGained")
    lost = raw.get("subscribersLost")
    engaged = raw.get("engagedViews")
    avg_pct = raw.get("averageViewPercentage")

    inter = None
    if None not in (likes, comments, shares):
        inter = likes + comments + shares

    return {
        "engaged_view_rate": _rate(engaged, views),
        "likes_per_1000_views": _rate(likes, views, 1000),
        "comments_per_1000_views": _rate(comments, views, 1000),
        "shares_per_1000_views": _rate(shares, views, 1000),
        "subs_per_1000_views": _rate(gained, views, 1000),
        "net_subs_per_1000_views": _rate((gained - lost) if None not in (gained, lost) else None, views, 1000),
        "interactions_per_1000_views": _rate(inter, views, 1000),
        "watch_percentage": (avg_pct / 100.0) if avg_pct is not None else None,
    }


def growth_between(older: dict, newer: dict) -> dict:
    """Crescimento entre dois snapshots (cada um com 'views'/'engaged_views'/
    'video_age_hours'). Fração de aumento e taxa por hora."""
    def pair(key):
        a, b = older.get(key), newer.get(key)
        if a is None or b is None:
            return None, None
        delta = b - a
        frac = (delta / a) if a > 0 else None
        dt = (newer.get("video_age_hours") or 0) - (older.get("video_age_hours") or 0)
        per_h = (delta / dt) if dt and dt > 0 else None
        return frac, per_h

    vf, vph = pair("views")
    ef, eph = pair("engaged_views")
    return {
        "views_growth_rate": vf,
        "views_per_hour": vph,
        "engaged_views_growth_rate": ef,
        "engaged_views_per_hour": eph,
    }


def quality_score(raw: dict, derived: dict | None = None, weights: dict | None = None) -> dict:
    """Score experimental em 0..1 + componentes. Pesos configuráveis
    (``config.quality_weights`` / env ``YOUTUBE_QUALITY_WEIGHTS``)."""
    d = derived or derived_metrics(raw)
    w = weights or cfg.quality_weights()

    def clip01(x):
        return None if x is None else max(0.0, min(1.0, x))

    comp = {
        "retention": clip01(d.get("watch_percentage")),
        "engaged_view_rate": clip01(d.get("engaged_view_rate")),
        "engagement": clip01(_rate(d.get("interactions_per_1000_views"), 1000.0 * ENGAGEMENT_CAP)),
        "subscriber_conversion": clip01(_rate(d.get("subs_per_1000_views"), SUBS_PER_1000_CAP)),
    }
    num = sum(w.get(k, 0.0) * v for k, v in comp.items() if v is not None)
    den = sum(w.get(k, 0.0) for k, v in comp.items() if v is not None)
    return {
        "quality_score": (num / den) if den > 0 else None,
        "components": comp,
        "weights": w,
        "missing": [k for k, v in comp.items() if v is None],
    }
