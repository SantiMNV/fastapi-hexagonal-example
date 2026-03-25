from sqlalchemy.orm import Session

from src.shared.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork
from src.users.application.ports.post_gateway import IPostGateway
from src.users.application.use_cases import (
    DeleteUserUseCase,
    GetUserUseCase,
    GetUserWithPostsUseCase,
    ListUserPostsUseCase,
    RegisterUserUseCase,
)
from src.users.infrastructure.persistence.repository import SQLAlchemyUserRepository


class UserFactory:
    def __init__(self, *, session: Session, post_gateway: IPostGateway) -> None:
        self._session = session
        self._uow = SQLAlchemyUnitOfWork(session)
        self._post_gateway = post_gateway

    def _users(self) -> SQLAlchemyUserRepository:
        return SQLAlchemyUserRepository(self._session)

    def create_register_user_use_case(self) -> RegisterUserUseCase:
        return RegisterUserUseCase(self._users(), self._uow)

    def create_get_user_use_case(self) -> GetUserUseCase:
        return GetUserUseCase(self._users())

    def create_delete_user_use_case(self) -> DeleteUserUseCase:
        return DeleteUserUseCase(self._users(), self._post_gateway, self._uow)

    def create_get_user_with_posts_use_case(self) -> GetUserWithPostsUseCase:
        return GetUserWithPostsUseCase(self._users(), self._post_gateway)

    def create_list_user_posts_use_case(self) -> ListUserPostsUseCase:
        return ListUserPostsUseCase(self._users(), self._post_gateway)
