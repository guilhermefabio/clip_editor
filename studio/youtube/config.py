"""Configuração e segredos do subsistema YouTube.

Ordem de resolução de cada credencial:
1. variável de ambiente (``YOUTUBE_CLIENT_ID`` etc.);
2. arquivo ``studio/youtube/secrets/youtube.env`` (``CHAVE=valor`` por linha);
3. arquivos padrão da lib do Google em ``secrets/`` (``client_secret.json``).

Segredos NUNCA ficam no código. A pasta ``secrets/`` está fora de versionamento.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SECRETS = HERE / "secrets"
SECRETS.mkdir(exist_ok=True)

ENV_FILE = SECRETS / "youtube.env"
CLIENT_SECRET_FILE = SECRETS / "client_secret.json"
TOKEN_FILE = SECRETS / "token.json"
DB_PATH = HERE / "metrics.db"
LINKS_JSON = HERE / "links.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]

# Janelas de snapshot por idade do vídeo (horas). period-of-study, não scheduler.
AGE_WINDOWS_HOURS = {"1h": 1, "6h": 6, "24h": 24, "72h": 72, "7d": 168, "28d": 672}
# tolerância para casar a idade atual com uma janela (horas)
WINDOW_TOLERANCE_HOURS = {"1h": 0.5, "6h": 1.5, "24h": 4, "72h": 8, "7d": 24, "28d": 72}

# Pesos do quality_score — experimentais, NÃO são verdade absoluta.
# views absolutas de propósito não entram como sinal isolado de qualidade.
QUALITY_WEIGHTS = {
    "retention": 0.40,            # average_view_percentage / 100
    "engaged_view_rate": 0.25,    # engaged_views / views
    "engagement": 0.20,           # (likes+comments+shares) / 1000 views, normalizado
    "subscriber_conversion": 0.15,  # subs_gained / 1000 views, normalizado
}


def _file_env() -> dict[str, str]:
    if not ENV_FILE.exists():
        return {}
    out = {}
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def get(name: str, default: str | None = None) -> str | None:
    return os.environ.get(name) or _file_env().get(name) or default


def credentials() -> dict:
    """Credenciais para o fluxo de refresh-token (server-to-server)."""
    return {
        "client_id": get("YOUTUBE_CLIENT_ID"),
        "client_secret": get("YOUTUBE_CLIENT_SECRET"),
        "refresh_token": get("YOUTUBE_REFRESH_TOKEN"),
        "channel_id": get("YOUTUBE_CHANNEL_ID"),  # opcional: senão usa mine=true
    }


def quality_weights() -> dict:
    raw = get("YOUTUBE_QUALITY_WEIGHTS")
    if raw:
        try:
            w = json.loads(raw)
            if isinstance(w, dict):
                return {**QUALITY_WEIGHTS, **{k: float(v) for k, v in w.items()}}
        except (json.JSONDecodeError, TypeError, ValueError):
            pass
    return dict(QUALITY_WEIGHTS)


def redact(value: str | None) -> str:
    if not value:
        return "<vazio>"
    return value[:4] + "…" + value[-2:] if len(value) > 8 else "…"
