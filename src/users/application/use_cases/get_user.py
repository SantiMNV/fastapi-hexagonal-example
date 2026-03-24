from __future__ import annotations

from src.users.application.ports.user_repository import IUserRepository
from src.users.domain.exceptions import UserNotFoundException
from src.users.domain.user import User


class GetUserUseCase:
    def __init__(self, repository: IUserRepository) -> None:
        self._repository = repository

    async def execute(self, user_id: str) -> User:
        user = await self._repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundException(user_id)
        return user
