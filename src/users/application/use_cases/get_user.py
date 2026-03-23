from __future__ import annotations

from src.users.application.ports.user_repository import UserRepository
from src.users.domain.exceptions import UserNotFoundException
from src.users.domain.user import User


class GetUserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def execute(self, user_id: str) -> User:
        user = self._repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundException(user_id)
        return user
