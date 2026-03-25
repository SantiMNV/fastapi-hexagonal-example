import pytest
from fastapi.testclient import TestClient

from src.shared.infrastructure.http.factory import AppFactory
from src.shared.infrastructure.settings import get_settings


class TestInternalRoutes:
    _HEADER = "X-Internal-Token"
    _KEY = "test-internal-api-key"

    def _headers(self) -> dict[str, str]:
        return {self._HEADER: self._KEY}

    def _register(self, client: TestClient) -> str:
        response = client.post(
            "/users",
            json={"name": "Internal Tester", "email": "internal-tester@example.com"},
        )
        assert response.status_code == 201
        return response.json()["id"]

    def test_internal_posts_list_401_without_token(self, client: TestClient) -> None:
        user_id = self._register(client)
        response = client.get("/internal/posts", params={"user_id": user_id})

        assert response.status_code == 401

    def test_internal_posts_list_401_wrong_token(self, client: TestClient) -> None:
        user_id = self._register(client)
        response = client.get(
            "/internal/posts",
            params={"user_id": user_id},
            headers={self._HEADER: "wrong"},
        )

        assert response.status_code == 401

    def test_internal_posts_list_ok(self, client: TestClient) -> None:
        user_id = self._register(client)
        response = client.get(
            "/internal/posts",
            params={"user_id": user_id},
            headers=self._headers(),
        )

        assert response.status_code == 200
        assert response.json() == []

    def test_internal_posts_delete_ok(self, client: TestClient) -> None:
        user_id = self._register(client)
        client.post(
            "/posts",
            json={"user_id": user_id, "title": "T", "content": "C"},
        )
        response = client.delete(
            "/internal/posts",
            params={"user_id": user_id},
            headers=self._headers(),
        )

        assert response.status_code == 204

    def test_internal_users_get_401_without_token(self, client: TestClient) -> None:
        user_id = self._register(client)
        response = client.get(f"/internal/users/{user_id}")

        assert response.status_code == 401

    def test_internal_users_get_ok(self, client: TestClient) -> None:
        user_id = self._register(client)
        response = client.get(f"/internal/users/{user_id}", headers=self._headers())

        assert response.status_code == 200
        assert response.json()["id"] == user_id


class TestHttpGatewaysRequireInternalKey:
    def test_app_factory_raises_without_internal_key_when_remote_posts(
        self, monkeypatch, db_session
    ) -> None:
        monkeypatch.setenv("POSTS_SERVICE_URL", "http://posts.example")
        monkeypatch.delenv("INTERNAL_API_KEY", raising=False)
        get_settings.cache_clear()
        try:
            with pytest.raises(ValueError, match="internal_api_key"):
                _ = AppFactory(session=db_session).users
        finally:
            get_settings.cache_clear()

    def test_app_factory_raises_without_internal_key_when_remote_users(
        self, monkeypatch, db_session
    ) -> None:
        monkeypatch.setenv("USERS_SERVICE_URL", "http://users.example")
        monkeypatch.delenv("INTERNAL_API_KEY", raising=False)
        get_settings.cache_clear()
        try:
            with pytest.raises(ValueError, match="internal_api_key"):
                _ = AppFactory(session=db_session).posts
        finally:
            get_settings.cache_clear()
