from fastapi import Depends, Request
from sqlalchemy.orm import Session

from src.shared.infrastructure.db import get_session

from .context import RequestContext
from .factory import AppFactory


def get_request_context(
    request: Request,
    session: Session = Depends(get_session),
) -> RequestContext:
    return RequestContext(
        request=request,
        session=session,
        factory=AppFactory(session=session),
    )
