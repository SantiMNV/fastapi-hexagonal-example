from sqlalchemy.orm import Session

from src.posts.infrastructure.http.factory import PostFactory
from src.users.infrastructure.http.factory import UserFactory


class AppFactory:
    """Global composition root: per-domain factories for one request session."""

    def __init__(self, *, session: Session) -> None:
        self.users = UserFactory(session=session)
        self.posts = PostFactory(session=session)
