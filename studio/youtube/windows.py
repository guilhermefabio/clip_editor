"""Quais janelas de idade (1h, 6h, 24h, 72h, 7d, 28d) coletar agora.

Uma janela só é "devida" quando a idade atual do vídeo está **perto** do alvo
(dentro da tolerância) e ela ainda não foi capturada. Se o vídeo já passou muito
do alvo sem captura, a janela é "perdida" — a Analytics é cumulativa até hoje,
então capturar tarde daria o número errado para aquela fatia de tempo.

Isto NÃO é um scheduler. É só a regra de decisão; quem agenda é o cron/CI.
"""
from __future__ import annotations

import sys
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from youtube import config as cfg  # noqa: E402
from youtube.util import parse_rfc3339, utcnow  # noqa: E402


def classify(age_hours: float | None, captured: set[str]) -> dict:
    """{'due': [...], 'missed': [...], 'pending': [...]} para uma idade dada."""
    due, missed, pending = [], [], []
    if age_hours is None:
        return {"due": [], "missed": [], "pending": list(cfg.AGE_WINDOWS_HOURS)}
    for name, target in cfg.AGE_WINDOWS_HOURS.items():
        if name in captured:
            continue
        tol = cfg.WINDOW_TOLERANCE_HOURS.get(name, target * 0.1)
        if age_hours < target - tol:
            pending.append(name)
        elif age_hours <= target + tol:
            due.append(name)
        else:
            missed.append(name)
    return {"due": due, "missed": missed, "pending": pending}


def window_date_range(published_at: str, window: str) -> tuple[str, str]:
    """Intervalo YYYY-MM-DD da publicação até o fim da janela (limitado a hoje)."""
    pub = parse_rfc3339(published_at)
    if pub is None:
        raise ValueError("published_at inválido")
    end = pub + timedelta(hours=cfg.AGE_WINDOWS_HOURS[window])
    today = utcnow()
    if end > today:
        end = today
    return pub.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


def next_check_hint(age_hours: float | None) -> str | None:
    """Nome da próxima janela ainda pendente — útil para logs/agendamento."""
    if age_hours is None:
        return next(iter(cfg.AGE_WINDOWS_HOURS))
    for name, target in cfg.AGE_WINDOWS_HOURS.items():
        if age_hours < target:
            return name
    return None
