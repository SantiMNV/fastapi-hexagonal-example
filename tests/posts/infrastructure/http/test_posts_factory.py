from sqlalchemy.orm import Session

from src.posts.application.use_cases import (
    CreatePostUseCase,
    DeletePostUseCase,
    GetPostUseCase,
    ListUserPostsUseCase,
)
from src.posts.infrastructure.http.factory import PostFactory
from src.posts.infrastructure.persistence.repository import SQLAlchemyPostRepository


class TestPostFactory:
    def test_create_use_cases(self, db_session: Session) -> None:
        factory = PostFactory(
            session=db_session,
            post_repository=SQLAlchemyPostRepository(db_session),
        )

        assert isinstance(factory.create_create_post_use_case(), CreatePostUseCase)
        assert isinstance(factory.create_get_post_use_case(), GetPostUseCase)
        assert isinstance(factory.create_list_user_posts_use_case(), ListUserPostsUseCase)
        assert isinstance(factory.create_delete_post_use_case(), DeletePostUseCase)
