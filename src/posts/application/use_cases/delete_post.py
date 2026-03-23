from __future__ import annotations

from src.posts.application.ports.post_repository import PostRepository
from src.posts.domain.exceptions import PostNotFoundException
from src.shared.application.ports.unit_of_work import UnitOfWork


class DeletePostUseCase:
    def __init__(self, repository: PostRepository, uow: UnitOfWork) -> None:
        self._repository = repository
        self._uow = uow

    def execute(self, post_id: str) -> None:
        existing = self._repository.get_by_id(post_id)
        if existing is None:
            raise PostNotFoundException(post_id)
        try:
            self._repository.delete(post_id)
            self._uow.commit()
        except Exception:
            self._uow.rollback()
            raise
