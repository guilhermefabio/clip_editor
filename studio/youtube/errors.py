"""Erros do subsistema YouTube, para tratamento explícito no collector."""


class YouTubeError(Exception):
    """Base."""


class AuthError(YouTubeError):
    """Token expirado, ausente ou autorização revogada."""


class QuotaError(YouTubeError):
    """Quota diária da API excedida (limite de uso, não custo financeiro)."""


class VideoUnavailableError(YouTubeError):
    """Vídeo privado, removido ou sem permissão."""


class MetricUnavailableError(YouTubeError):
    """Métrica pedida não foi retornada pela API para este vídeo/intervalo."""


class TransientAPIError(YouTubeError):
    """Timeout ou 5xx — vale a pena repetir."""
