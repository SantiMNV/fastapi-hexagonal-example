from sqlalchemy.orm import Session

from src.posts.infrastructure.persistence.repository import SQLAlchemyPostRepository
from src.shared.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork
from src.users.application.use_cases import (
    DeleteUserUseCase,
    GetUserUseCase,
    GetUserWithPostsUseCase,
    RegisterUserUseCase,
)
from src.users.infrastructure.persistence.repository import SQLAlchemyUserRepository


class UserFactory:
    """User bounded context: use cases wired for one request session."""

    def __init__(self, *, session: Session) -> None:
        self._session = session
        self._uow = SQLAlchemyUnitOfWork(session)

    def _users(self) -> SQLAlchemyUserRepository:
        return SQLAlchemyUserRepository(self._session)

    def _posts(self) -> SQLAlchemyPostRepository:
        return SQLAlchemyPostRepository(self._session)

    def create_register_user_use_case(self) -> RegisterUserUseCase:
        return RegisterUserUseCase(self._users(), self._uow)

    def create_get_user_use_case(self) -> GetUserUseCase:
        return GetUserUseCase(self._users())

    def create_delete_user_use_case(self) -> DeleteUserUseCase:
        return DeleteUserUseCase(self._users(), self._uow)

    def create_get_user_with_posts_use_case(self) -> GetUserWithPostsUseCase:
        return GetUserWithPostsUseCase(self._users(), self._posts())
