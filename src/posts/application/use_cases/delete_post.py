from __future__ import annotations

from src.posts.application.ports.post_repository import IPostRepository
from src.posts.domain.exceptions import PostNotFoundException
from src.shared.application.ports.unit_of_work import UnitOfWork


class DeletePostUseCase:

    def __init__(self, repository: IPostRepository, uow: UnitOfWork) -> None:
        self._repository = repository
        self._uow = uow

    async def execute(self, post_id: str) -> None:
        existing = await self._repository.get_by_id(post_id)
        if existing is None:
            raise PostNotFoundException(post_id)
        try:
            await self._repository.delete(post_id)
            self._uow.commit()
        except Exception:
            self._uow.rollback()
            raise
