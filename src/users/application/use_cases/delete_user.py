from __future__ import annotations

from src.shared.application.ports.unit_of_work import UnitOfWork
from src.users.application.ports.user_repository import UserRepository
from src.users.domain.exceptions import UserNotFoundException


class DeleteUserUseCase:
    def __init__(self, repository: UserRepository, uow: UnitOfWork) -> None:
        self._repository = repository
        self._uow = uow

    def execute(self, user_id: str) -> None:
        existing = self._repository.get_by_id(user_id)
        if existing is None:
            raise UserNotFoundException(user_id)
        try:
            self._repository.delete(user_id)
            self._uow.commit()
        except Exception:
            self._uow.rollback()
            raise
