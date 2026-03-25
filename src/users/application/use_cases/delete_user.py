from __future__ import annotations

from src.shared.application.ports.unit_of_work import UnitOfWork
from src.users.application.ports.post_gateway import IPostGateway
from src.users.application.ports.user_repository import IUserRepository
from src.users.domain.exceptions import UserNotFoundException


class DeleteUserUseCase:
    def __init__(
        self,
        repository: IUserRepository,
        post_gateway: IPostGateway,
        uow: UnitOfWork,
    ) -> None:
        self._repository = repository
        self._post_gateway = post_gateway
        self._uow = uow

    async def execute(self, user_id: str) -> None:
        existing = await self._repository.get_by_id(user_id)
        if existing is None:
            raise UserNotFoundException(user_id)
        await self._post_gateway.delete_by_user_id(user_id)
        try:
            await self._repository.delete(user_id)
            self._uow.commit()
        except Exception:
            self._uow.rollback()
            raise
