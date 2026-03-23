from datetime import UTC, datetime
from uuid import uuid4

from src.posts.domain.post import Post
from tests.users.doubles import (
    InMemoryPostRepository,
    InMemoryUserRepository,
    NoOpUnitOfWork,
    sample_user,
)

__all__ = [
    "InMemoryPostRepository",
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
