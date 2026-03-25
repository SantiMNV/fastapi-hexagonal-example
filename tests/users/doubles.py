from datetime import UTC, datetime
from uuid import uuid4

from src.posts.application.ports.post_repository import IPostRepository
from src.posts.domain.post import Post
from src.shared.application.ports.unit_of_work import UnitOfWork
from src.users.application.ports.post_gateway import IPostGateway
from src.users.application.ports.user_repository import IUserRepository
from src.users.domain.post_snapshot import PostSnapshot
from src.users.domain.user import User


class NoOpUnitOfWork(UnitOfWork):
    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


class InMemoryUserRepository(IUserRepository):
    def __init__(self) -> None:
        self.users: dict[str, User] = {}

    async def add(self, user: User) -> None:
        self.users[user.id] = user

    async def get_by_id(self, user_id: str) -> User | None:
        return self.users.get(user_id)

    async def get_by_email(self, email: str) -> User | None:
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    async def delete(self, user_id: str) -> None:
        self.users.pop(user_id, None)


class InMemoryPostRepository(IPostRepository):
    def __init__(self) -> None:
        self.posts: dict[str, Post] = {}

    async def add(self, post: Post) -> None:
        self.posts[post.id] = post

    async def get_by_id(self, post_id: str) -> Post | None:
        return self.posts.get(post_id)

    async def list_by_user_id(self, user_id: str) -> list[Post]:
        return [p for p in self.posts.values() if p.user_id == user_id]

    async def delete(self, post_id: str) -> None:
        self.posts.pop(post_id, None)

    async def delete_by_user_id(self, user_id: str) -> None:
        for post_id, post in list(self.posts.items()):
            if post.user_id == user_id:
                del self.posts[post_id]


class InMemoryPostGateway(IPostGateway):
    """Test double for IPostGateway backed by InMemoryPostRepository."""

    def __init__(self, repository: InMemoryPostRepository | None = None) -> None:
        self._repo = repository or InMemoryPostRepository()

    async def list_by_user_id(self, user_id: str) -> list[PostSnapshot]:
        posts = await self._repo.list_by_user_id(user_id)
        return [
            PostSnapshot(
                id=p.id,
                user_id=p.user_id,
                title=p.title,
                content=p.content,
                created_at=p.created_at,
            )
            for p in posts
        ]

    async def delete_by_user_id(self, user_id: str) -> None:
        await self._repo.delete_by_user_id(user_id)


def sample_user(*, user_id: str | None = None, email: str = "alice@example.com") -> User:
    return User(
        id=user_id or str(uuid4()),
        name="Alice",
        email=email,
        created_at=datetime.now(UTC),
    )
