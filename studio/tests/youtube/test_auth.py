"""Renovação e falha de autenticação — credenciais falsas, sem rede."""
import pytest
from youtube import auth
from youtube.errors import AuthError


class FakeCreds:
    def __init__(self, valid=False, raise_on_refresh=False):
        self._valid = valid
        self._raise = raise_on_refresh
        self.refreshed = False
        self.expiry = None
        self.refresh_token = "rt-secret"
    @property
    def valid(self):
        return self._valid
    def refresh(self, _request):
        from google.auth.exceptions import RefreshError
        if self._raise:
            raise RefreshError("invalid_grant")
        self.refreshed = True
        self._valid = True
    def to_json(self):
        return "{}"


def test_refreshes_when_invalid(monkeypatch, tmp_path):
    fake = FakeCreds(valid=False)
    monkeypatch.setattr(auth, "_from_env", lambda: fake)
    monkeypatch.setattr(auth.cfg, "TOKEN_FILE", tmp_path / "none.json")
    creds = auth.load_credentials()
    assert creds is fake and fake.refreshed is True


def test_no_refresh_when_valid(monkeypatch):
    fake = FakeCreds(valid=True)
    monkeypatch.setattr(auth, "_from_env", lambda: fake)
    creds = auth.load_credentials()
    assert creds.refreshed is False


def test_revoked_token_raises_autherror(monkeypatch):
    monkeypatch.setattr(auth, "_from_env", lambda: FakeCreds(valid=False, raise_on_refresh=True))
    with pytest.raises(AuthError):
        auth.load_credentials()


def test_missing_credentials_raises(monkeypatch):
    monkeypatch.setattr(auth, "_from_env", lambda: None)
    monkeypatch.setattr(auth, "_from_token_file", lambda: None)
    with pytest.raises(AuthError):
        auth.load_credentials()


def test_log_redactor_hides_secret():
    from youtube.log import _Redactor
    import logging
    rec = logging.LogRecord("youtube.auth", logging.INFO, "f", 1,
                            "refresh_token=abc123 client_secret=zzz", None, None)
    _Redactor().filter(rec)
    assert "abc123" not in rec.msg and "zzz" not in rec.msg
    assert "***" in rec.msg
