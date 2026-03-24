from sqlalchemy.orm import Session

from src.posts.application.ports.post_repository import IPostRepository
from src.posts.application.use_cases import (
    CreatePostUseCase,
    DeletePostUseCase,
    GetPostUseCase,
    ListUserPostsUseCase,
)
from src.shared.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork
from src.users.infrastructure.persistence.repository import SQLAlchemyUserRepository


class PostFactory:
    """Posts bounded context: use cases wired for one request session."""

    def __init__(self, *, session: Session, post_repository: IPostRepository) -> None:
        self._session = session
        self._uow = SQLAlchemyUnitOfWork(session)
        self._post_repository = post_repository

    def _posts(self) -> IPostRepository:
        return self._post_repository

    def _users(self) -> SQLAlchemyUserRepository:
        return SQLAlchemyUserRepository(self._session)

    def create_create_post_use_case(self) -> CreatePostUseCase:
        return CreatePostUseCase(self._posts(), self._users(), self._uow)

    def create_get_post_use_case(self) -> GetPostUseCase:
        return GetPostUseCase(self._posts())

    def create_list_user_posts_use_case(self) -> ListUserPostsUseCase:
        return ListUserPostsUseCase(self._posts(), self._users())

    def create_delete_post_use_case(self) -> DeletePostUseCase:
        return DeletePostUseCase(self._posts(), self._uow)
