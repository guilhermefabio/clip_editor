"""OAuth 2.0 para a conta do próprio canal.

Dois caminhos:

* **bootstrap** (uma vez, máquina com navegador)::

      python studio/youtube/auth.py login

  Abre o consentimento, grava ``secrets/token.json`` e imprime o
  ``refresh_token`` para você colocar em ``YOUTUBE_REFRESH_TOKEN``.

* **runtime**: :func:`load_credentials` monta as credenciais a partir das
  variáveis de ambiente (``YOUTUBE_CLIENT_ID`` / ``_SECRET`` / ``_REFRESH_TOKEN``)
  ou de ``secrets/token.json``, e renova o access token sozinho.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from youtube import config as cfg  # noqa: E402
from youtube.errors import AuthError  # noqa: E402
from youtube.log import E_AUTH_OK, get_logger  # noqa: E402

log = get_logger("youtube.auth")


def _from_env():
    from google.oauth2.credentials import Credentials

    c = cfg.credentials()
    if not (c["client_id"] and c["client_secret"] and c["refresh_token"]):
        return None
    return Credentials(
        token=None,
        refresh_token=c["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=c["client_id"],
        client_secret=c["client_secret"],
        scopes=cfg.SCOPES,
    )


def _from_token_file():
    from google.oauth2.credentials import Credentials

    if not cfg.TOKEN_FILE.exists():
        return None
    return Credentials.from_authorized_user_file(str(cfg.TOKEN_FILE), cfg.SCOPES)


def load_credentials(*, allow_interactive: bool = False):
    """Credenciais válidas e atualizadas, ou :class:`AuthError`."""
    from google.auth.exceptions import RefreshError
    from google.auth.transport.requests import Request

    creds = _from_env() or _from_token_file()
    if creds is None:
        if allow_interactive and cfg.CLIENT_SECRET_FILE.exists():
            return _interactive_login()
        raise AuthError(
            "Sem credenciais. Defina YOUTUBE_CLIENT_ID/SECRET/REFRESH_TOKEN "
            "ou rode: python studio/youtube/auth.py login"
        )
    try:
        if not creds.valid:
            creds.refresh(Request())
    except RefreshError as exc:
        raise AuthError(f"Falha ao renovar token (revogado/expirado?): {exc}") from exc

    if cfg.TOKEN_FILE.exists():  # mantém o cache local fresco
        try:
            cfg.TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
        except OSError:
            pass
    log.info("%s scopes=%s", E_AUTH_OK, ",".join(cfg.SCOPES))
    return creds


def _interactive_login():
    from google_auth_oauthlib.flow import InstalledAppFlow

    flow = InstalledAppFlow.from_client_secrets_file(str(cfg.CLIENT_SECRET_FILE), cfg.SCOPES)
    creds = flow.run_local_server(port=0, prompt="consent")
    cfg.TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    log.info("%s (bootstrap)", E_AUTH_OK)
    print("\ntoken salvo em:", cfg.TOKEN_FILE)
    print("Coloque este valor em YOUTUBE_REFRESH_TOKEN (ou deixe o token.json):")
    print("  ", creds.refresh_token)
    return creds


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "login":
        _interactive_login()
    else:
        c = load_credentials()
        print("credenciais OK — token válido:", c.valid, "| expira:", c.expiry)
