from fastapi.testclient import TestClient


class TestCreateAppScaffolding:
    """Smoke test: `conftest` `app`/`client` match `src.shared.main.create_app` + lifespan."""

    def test_openapi_loads_after_lifespan(self, client: TestClient) -> None:
        response = client.get("/openapi.json")

        assert response.status_code == 200
        assert "openapi" in response.json()
