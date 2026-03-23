from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

from src.shared.infrastructure.db import get_session


class TestGetSession:
    def _app_with_session_factory(self, factory: sessionmaker[Session]) -> FastAPI:
        app = FastAPI()
        app.state.session_factory = factory

        @app.get("/db")
        def touch_db(_session: Session = Depends(get_session)) -> dict[str, bool]:
            return {"ok": True}

        return app

    def test_yields_session_from_app_state(self, session_factory: sessionmaker[Session]) -> None:
        app = self._app_with_session_factory(session_factory)

        with TestClient(app) as test_client:
            response = test_client.get("/db")

        assert response.status_code == 200
        assert response.json() == {"ok": True}
