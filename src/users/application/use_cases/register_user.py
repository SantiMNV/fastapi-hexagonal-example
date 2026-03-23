from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from src.shared.application.ports.unit_of_work import UnitOfWork
from src.users.application.ports.user_repository import UserRepository
from src.users.domain.exceptions import UserAlreadyExistsException
from src.users.domain.user import User


class RegisterUserUseCase:
    def __init__(self, repository: UserRepository, uow: UnitOfWork) -> None:
        self._repository = repository
        self._uow = uow

    def execute(self, name: str, email: str) -> User:
        existing = self._repository.get_by_email(email)
        if existing is not None:
            raise UserAlreadyExistsException(email)

        user = User(
            id=str(uuid4()),
            name=name,
            email=email,
            created_at=datetime.now(UTC),
        )
        try:
            self._repository.add(user)
            self._uow.commit()
        except Exception:
            self._uow.rollback()
            raise
        return user
