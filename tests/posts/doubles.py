from datetime import UTC, datetime
from uuid import uuid4

from src.posts.application.ports.user_gateway import IUserGateway
from src.posts.domain.post import Post
from src.posts.domain.user_snapshot import UserSnapshot
from tests.users.doubles import (
    InMemoryPostGateway,
    InMemoryPostRepository,
    InMemoryUserRepository,
    NoOpUnitOfWork,
    sample_user,
)


class InMemoryUserGateway(IUserGateway):
    def __init__(self) -> None:
        self.snapshots: dict[str, UserSnapshot] = {}

    async def get_by_id(self, user_id: str) -> UserSnapshot | None:
        return self.snapshots.get(user_id)


__all__ = [
    "InMemoryPostGateway",
    "InMemoryPostRepository",
    "InMemoryUserGateway",
    "InMemoryUserRepository",
    "NoOpUnitOfWork",
    "sample_post",
    "sample_user",
]


def sample_post(
    *,
    post_id: str | None = None,
    user_id: str,
    title: str = "Title",
    content: str = "Content",
) -> Post:
    return Post(
        id=post_id or str(uuid4()),
        user_id=user_id,
        title=title,
        content=content,
        created_at=datetime.now(UTC),
    )
