from datetime import timedelta

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
from src.users.application.use_cases.verify_user_can_create_post import (
    VerifyUserCanCreatePostUseCase,
)
from src.users.infrastructure.persistence.repository import SQLAlchemyUserRepository


class UserFactory:
    def __init__(
        self,
        *,
        session: Session,
        post_gateway: IPostGateway,
        min_account_age: timedelta,
    ) -> None:
        self._session = session
        self._uow = SQLAlchemyUnitOfWork(session)
        self._post_gateway = post_gateway
        self._min_account_age = min_account_age
        self._user_repository = SQLAlchemyUserRepository(self._session)

    def create_register_user_use_case(self) -> RegisterUserUseCase:
        return RegisterUserUseCase(self._user_repository, self._uow)

    def create_get_user_use_case(self) -> GetUserUseCase:
        return GetUserUseCase(self._user_repository)

    def create_verify_user_can_create_post_use_case(
        self,
    ) -> VerifyUserCanCreatePostUseCase:
        return VerifyUserCanCreatePostUseCase(
            self._user_repository,
            min_account_age=self._min_account_age,
        )

    def create_delete_user_use_case(self) -> DeleteUserUseCase:
        return DeleteUserUseCase(self._user_repository, self._post_gateway, self._uow)

    def create_get_user_with_posts_use_case(self) -> GetUserWithPostsUseCase:
        return GetUserWithPostsUseCase(self._user_repository, self._post_gateway)

    def create_list_user_posts_use_case(self) -> ListUserPostsUseCase:
        return ListUserPostsUseCase(self._user_repository, self._post_gateway)
