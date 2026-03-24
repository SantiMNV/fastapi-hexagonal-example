from sqlalchemy.orm import Session

from src.posts.application.ports.post_repository import IPostRepository
from src.posts.infrastructure.http.factory import PostFactory
from src.users.infrastructure.http.factory import UserFactory


class AppFactory:
    """Global composition root: per-domain factories for one request session."""

    def __init__(self, *, session: Session, post_repository: IPostRepository) -> None:
        self.users = UserFactory(session=session, post_repository=post_repository)
        self.posts = PostFactory(session=session, post_repository=post_repository)
