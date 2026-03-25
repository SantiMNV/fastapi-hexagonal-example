from fastapi import Depends, Request
from sqlalchemy.orm import Session

from src.shared.infrastructure.db import get_session
from src.shared.infrastructure.http.context import RequestContext
from src.shared.infrastructure.http.factory import AppFactory


def get_app_factory(session: Session = Depends(get_session)) -> AppFactory:
    return AppFactory(session=session)


def get_request_context(
    request: Request,
    session: Session = Depends(get_session),
) -> RequestContext:
    return RequestContext(
        request=request,
        session=session,
        factory=AppFactory(session=session),
    )
