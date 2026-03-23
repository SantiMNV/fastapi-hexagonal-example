from dataclasses import dataclass

from fastapi import Request
from sqlalchemy.orm import Session

from .factory import AppFactory


@dataclass(slots=True)
class RequestContext:
    """Per-request scope: HTTP request, DB session, and global app factory."""

    request: Request
    session: Session
    factory: AppFactory
