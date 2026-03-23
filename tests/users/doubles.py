from datetime import UTC, datetime
from uuid import uuid4

from src.users.application.ports.user_repository import UserRepository
from src.users.domain.user import User


class NoOpUnitOfWork:
    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self.users: dict[str, User] = {}

    def add(self, user: User) -> None:
        self.users[user.id] = user

    def get_by_id(self, user_id: str) -> User | None:
        return self.users.get(user_id)

    def get_by_email(self, email: str) -> User | None:
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def delete(self, user_id: str) -> None:
        self.users.pop(user_id, None)


def sample_user(*, user_id: str | None = None, email: str = "alice@example.com") -> User:
    return User(
        id=user_id or str(uuid4()),
        name="Alice",
        email=email,
        created_at=datetime.now(UTC),
    )
