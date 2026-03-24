from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.posts.infrastructure.persistence.repository import SQLAlchemyPostRepository
from src.shared.infrastructure.http.context import RequestContext
from src.shared.infrastructure.http.factory import AppFactory


class TestRequestContext:
    def test_holds_request_session_and_factory(self, db_session: Session) -> None:
        request = MagicMock()
        factory = AppFactory(
            session=db_session,
            post_repository=SQLAlchemyPostRepository(db_session),
        )
        ctx = RequestContext(request=request, session=db_session, factory=factory)

        assert ctx.request is request
        assert ctx.session is db_session
        assert ctx.factory is factory
