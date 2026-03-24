from fastapi import Depends, Request
from sqlalchemy.orm import Session

from src.posts.infrastructure.http.post_repository_gateway import PostRepositoryGateway
from src.posts.infrastructure.persistence.repository import SQLAlchemyPostRepository
from src.shared.infrastructure.db import get_session
from src.shared.infrastructure.settings import get_settings

from .context import RequestContext
from .factory import AppFactory


def get_request_context(
    request: Request,
    session: Session = Depends(get_session),
) -> RequestContext:
    settings = get_settings()
    if settings.post_service_external:
        client = getattr(request.app.state, "posts_http_client", None)
        if client is None:
            msg = "posts_http_client is required when post_service_external is true"
            raise RuntimeError(msg)
        post_repository = PostRepositoryGateway(
            client=client,
            base_url=settings.posts_service_base_url,
        )
    else:
        post_repository = SQLAlchemyPostRepository(session)

    return RequestContext(
        request=request,
        session=session,
        factory=AppFactory(session=session, post_repository=post_repository),
    )
