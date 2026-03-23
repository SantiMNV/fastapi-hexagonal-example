from datetime import UTC, datetime
from uuid import uuid4

from src.posts.application.ports.post_repository import PostRepository
from src.posts.domain.post import Post
from tests.users.doubles import InMemoryUserRepository, NoOpUnitOfWork, sample_user


class InMemoryPostRepository(PostRepository):
    def __init__(self) -> None:
        self.posts: dict[str, Post] = {}

    def add(self, post: Post) -> None:
        self.posts[post.id] = post

    def get_by_id(self, post_id: str) -> Post | None:
        return self.posts.get(post_id)

    def list_by_user_id(self, user_id: str) -> list[Post]:
        return [p for p in self.posts.values() if p.user_id == user_id]

    def delete(self, post_id: str) -> None:
        self.posts.pop(post_id, None)


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
