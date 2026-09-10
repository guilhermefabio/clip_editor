"""Service objects do YouTube (Data v3 + Analytics v2) com retry/backoff
e tradução dos erros HTTP para as exceções de :mod:`youtube.errors`.
"""
from __future__ import annotations

import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from youtube.errors import (  # noqa: E402
    QuotaError, TransientAPIError, VideoUnavailableError, YouTubeError,
)
from youtube.log import E_API_ERROR, E_QUOTA_ERROR, get_logger  # noqa: E402

log = get_logger("youtube.client")

_QUOTA_REASONS = {"quotaExceeded", "dailyLimitExceeded"}
_RATE_REASONS = {"rateLimitExceeded", "userRateLimitExceeded", "backendError", "internalError"}


class YouTubeClient:
    def __init__(self, credentials=None):
        from googleapiclient.discovery import build

        if credentials is None:
            from youtube.auth import load_credentials
            credentials = load_credentials()
        self.creds = credentials
        self.data = build("youtube", "v3", credentials=credentials, cache_discovery=False)
        self.analytics = build("youtubeAnalytics", "v2", credentials=credentials,
                               cache_discovery=False)

    # -- execução resiliente -------------------------------------------------
    def execute(self, request, *, retries: int = 4):
        from googleapiclient.errors import HttpError

        for attempt in range(retries + 1):
            try:
                return request.execute()
            except HttpError as exc:
                status = getattr(exc, "status_code", None) or exc.resp.status
                reason = _reason(exc)
                if status == 403 and reason in _QUOTA_REASONS:
                    log.error("%s reason=%s", E_QUOTA_ERROR, reason)
                    raise QuotaError(f"Quota da API excedida ({reason}).") from exc
                if status == 404:
                    raise VideoUnavailableError("Recurso 404 (privado/removido).") from exc
                if status in (429, 500, 503) or reason in _RATE_REASONS:
                    if attempt < retries:
                        wait = min(60, 2 ** attempt) + random.uniform(0, 1)
                        log.warning("%s status=%s reason=%s retry em %.1fs",
                                    E_API_ERROR, status, reason, wait)
                        time.sleep(wait)
                        continue
                    raise TransientAPIError(f"API instável ({status}/{reason}).") from exc
                log.error("%s status=%s reason=%s", E_API_ERROR, status, reason)
                raise YouTubeError(f"Erro da API ({status}/{reason}).") from exc
            except (TimeoutError, ConnectionError, OSError) as exc:
                if attempt < retries:
                    wait = min(60, 2 ** attempt) + random.uniform(0, 1)
                    log.warning("%s rede: %s — retry em %.1fs", E_API_ERROR, exc, wait)
                    time.sleep(wait)
                    continue
                raise TransientAPIError(f"Rede: {exc}") from exc


def _reason(exc) -> str:
    try:
        errors = exc.error_details or []
        if errors and isinstance(errors, list):
            return errors[0].get("reason", "") or ""
    except Exception:  # noqa: BLE001
        pass
    try:
        import json
        body = json.loads(exc.content.decode("utf-8"))
        return body["error"]["errors"][0].get("reason", "")
    except Exception:  # noqa: BLE001
        return ""
