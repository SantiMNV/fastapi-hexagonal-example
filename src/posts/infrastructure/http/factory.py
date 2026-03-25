from sqlalchemy.orm import Session

from src.posts.application.ports.user_gateway import IUserGateway
from src.posts.application.use_cases import (
    CreatePostUseCase,
    DeletePostUseCase,
    DeleteUserPostsUseCase,
    GetPostsByUserUseCase,
    GetPostUseCase,
)
from src.posts.infrastructure.persistence.repository import SQLAlchemyPostRepository
from src.shared.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork


class PostFactory:
    def __init__(self, *, session: Session, user_gateway: IUserGateway) -> None:
        self._session = session
        self._uow = SQLAlchemyUnitOfWork(session)
        self._user_gateway = user_gateway

    def _posts(self) -> SQLAlchemyPostRepository:
        return SQLAlchemyPostRepository(self._session)

    def create_create_post_use_case(self) -> CreatePostUseCase:
        return CreatePostUseCase(self._posts(), self._user_gateway, self._uow)

    def create_get_post_use_case(self) -> GetPostUseCase:
        return GetPostUseCase(self._posts())

    def create_get_posts_by_user_use_case(self) -> GetPostsByUserUseCase:
        return GetPostsByUserUseCase(self._posts())

    def create_delete_post_use_case(self) -> DeletePostUseCase:
        return DeletePostUseCase(self._posts(), self._uow)

    def create_delete_user_posts_use_case(self) -> DeleteUserPostsUseCase:
        return DeleteUserPostsUseCase(self._posts(), self._uow)
