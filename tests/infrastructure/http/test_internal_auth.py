import logging

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from src.shared.infrastructure.http.internal_auth import (
    _constant_time_token_equal,
    verify_internal_api_key,
)
from src.shared.infrastructure.settings import get_settings


def _app_with_internal_auth() -> FastAPI:
    app = FastAPI()

    @app.get("/internal/ping")
    async def ping(_: None = Depends(verify_internal_api_key)) -> dict[str, str]:
        return {"status": "ok"}

    return app


class TestConstantTimeTokenEqual:
    def test_accepts_matching_secret(self) -> None:
        assert _constant_time_token_equal("same-secret", "same-secret") is True

    def test_rejects_different_secret(self) -> None:
        assert _constant_time_token_equal("expected", "wrong") is False

    def test_rejects_none_as_provided(self) -> None:
        assert _constant_time_token_equal("secret", None) is False

    def test_rejects_empty_provided_when_expected_non_empty(self) -> None:
        assert _constant_time_token_equal("secret", "") is False


class TestVerifyInternalApiKey:
    _KEY = "test-internal-api-key"
    _HEADER = "X-Internal-Token"

    def test_503_when_key_not_configured(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("INTERNAL_API_KEY", raising=False)
        get_settings.cache_clear()
        try:
            app = _app_with_internal_auth()
            with TestClient(app) as client:
                response = client.get(
                    "/internal/ping",
                    headers={self._HEADER: self._KEY},
                )
            assert response.status_code == 503
            assert response.json()["detail"] == "Internal API is not configured"
        finally:
            get_settings.cache_clear()

    def test_503_when_key_is_whitespace_only(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("INTERNAL_API_KEY", "   ")
        get_settings.cache_clear()
        try:
            app = _app_with_internal_auth()
            with TestClient(app) as client:
                response = client.get(
                    "/internal/ping",
                    headers={self._HEADER: "x"},
                )
            assert response.status_code == 503
        finally:
            get_settings.cache_clear()

    def test_401_when_header_missing(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("INTERNAL_API_KEY", self._KEY)
        get_settings.cache_clear()
        try:
            app = _app_with_internal_auth()
            with TestClient(app) as client:
                response = client.get("/internal/ping")
            assert response.status_code == 401
            assert response.json()["detail"] == "Invalid or missing internal credentials"
        finally:
            get_settings.cache_clear()

    def test_401_when_header_wrong(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("INTERNAL_API_KEY", self._KEY)
        get_settings.cache_clear()
        try:
            app = _app_with_internal_auth()
            with TestClient(app) as client:
                response = client.get(
                    "/internal/ping",
                    headers={self._HEADER: "wrong"},
                )
            assert response.status_code == 401
        finally:
            get_settings.cache_clear()

    def test_200_when_header_valid(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("INTERNAL_API_KEY", self._KEY)
        get_settings.cache_clear()
        try:
            app = _app_with_internal_auth()
            with TestClient(app) as client:
                response = client.get(
                    "/internal/ping",
                    headers={self._HEADER: self._KEY},
                )
            assert response.status_code == 200
            assert response.json() == {"status": "ok"}
        finally:
            get_settings.cache_clear()

    def test_respects_custom_header_name(self, monkeypatch: pytest.MonkeyPatch) -> None:
        custom = "X-Custom-Internal"
        monkeypatch.setenv("INTERNAL_API_KEY", self._KEY)
        monkeypatch.setenv("INTERNAL_API_HEADER_NAME", custom)
        get_settings.cache_clear()
        try:
            app = _app_with_internal_auth()
            with TestClient(app) as client:
                no_custom = client.get(
                    "/internal/ping",
                    headers={self._HEADER: self._KEY},
                )
                with_custom = client.get(
                    "/internal/ping",
                    headers={custom: self._KEY},
                )
            assert no_custom.status_code == 401
            assert with_custom.status_code == 200
        finally:
            get_settings.cache_clear()

    def test_logs_warning_on_auth_failure(
        self,
        monkeypatch: pytest.MonkeyPatch,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        monkeypatch.setenv("INTERNAL_API_KEY", self._KEY)
        get_settings.cache_clear()
        try:
            app = _app_with_internal_auth()
            with TestClient(app) as client, caplog.at_level(logging.WARNING):
                client.get("/internal/ping")
            assert any("internal API auth failed" in r.getMessage() for r in caplog.records)
            assert getattr(caplog.records[-1], "path", None) == "/internal/ping"
        finally:
            get_settings.cache_clear()
