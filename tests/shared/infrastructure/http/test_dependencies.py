from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

from src.shared.infrastructure.http.context import RequestContext
from src.shared.infrastructure.http.dependencies import get_request_context


class TestGetRequestContext:
    def _app_with_session_factory(self, factory: sessionmaker[Session]) -> FastAPI:
        app = FastAPI()
        app.state.session_factory = factory

        @app.get("/ctx")
        def read_ctx(ctx: RequestContext = Depends(get_request_context)) -> dict[str, bool]:
            return {
                "has_session": ctx.session is not None,
                "has_factory": ctx.factory is not None,
            }

        return app

    def test_builds_context_with_factory(self, session_factory: sessionmaker[Session]) -> None:
        app = self._app_with_session_factory(session_factory)

        with TestClient(app) as test_client:
            response = test_client.get("/ctx")

        assert response.status_code == 200
        assert response.json() == {
            "has_session": True,
            "has_factory": True,
        }
