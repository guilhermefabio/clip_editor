"""Logger namespeado + redação de segredos.

Nunca loga client_secret / access_token / refresh_token: o filtro abaixo
substitui qualquer ocorrência por ``***``.
"""
from __future__ import annotations

import logging
import re

_SECRET_RE = re.compile(
    r"(refresh_token|access_token|client_secret|token)[\"']?\s*[:=]\s*[\"']?([A-Za-z0-9._\-]+)",
    re.IGNORECASE,
)

# Eventos padronizados
E_AUTH_OK = "youtube.auth.success"
E_COLLECT_VIDEO = "youtube.collect.video"
E_COLLECT_ANALYTICS = "youtube.collect.analytics"
E_SNAPSHOT = "youtube.snapshot.created"
E_API_ERROR = "youtube.api.error"
E_QUOTA_ERROR = "youtube.quota.error"


class _Redactor(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = _SECRET_RE.sub(r"\1=***", record.msg)
        return True


def get_logger(name: str) -> logging.Logger:
    log = logging.getLogger(name if name.startswith("youtube") else f"youtube.{name}")
    if not any(isinstance(f, _Redactor) for f in log.filters):
        log.addFilter(_Redactor())
    if not logging.getLogger("youtube").handlers:
        h = logging.StreamHandler()
        h.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))
        logging.getLogger("youtube").addHandler(h)
        logging.getLogger("youtube").setLevel(logging.INFO)
    return log
