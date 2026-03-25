from __future__ import annotations

from src.posts.application.ports.post_repository import IPostRepository
from src.shared.application.ports.unit_of_work import UnitOfWork


class DeleteUserPostsUseCase:
    def __init__(self, post_repository: IPostRepository, uow: UnitOfWork) -> None:
        self._post_repository = post_repository
        self._uow = uow

    async def execute(self, user_id: str) -> None:
        try:
            await self._post_repository.delete_by_user_id(user_id)
            self._uow.commit()
        except Exception:
            self._uow.rollback()
            raise
