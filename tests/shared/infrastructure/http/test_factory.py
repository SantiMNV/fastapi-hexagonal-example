from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

from src.shared.infrastructure.http.context import RequestContext
from src.shared.infrastructure.http.dependencies import get_request_context
from src.shared.infrastructure.http.factory import AppFactory


class TestAppFactory:
    def test_exposes_user_and_post_factories(self, db_session: Session) -> None:
        factory = AppFactory(session=db_session)

        assert factory.users is not None
        assert factory.posts is not None

    def test_request_context_uses_domain_factories(
        self, session_factory: sessionmaker[Session]
    ) -> None:
        app = FastAPI()
        app.state.session_factory = session_factory

        @app.get("/inspect")
        def inspect(
            ctx: RequestContext = Depends(get_request_context),
        ) -> dict[str, str]:
            return {
                "factory_users": type(ctx.factory.users).__name__,
                "factory_posts": type(ctx.factory.posts).__name__,
            }

        with TestClient(app) as test_client:
            response = test_client.get("/inspect")

        assert response.status_code == 200
        body = response.json()
        assert body["factory_users"] == "UserFactory"
        assert body["factory_posts"] == "PostFactory"
