from sqlalchemy.orm import Session

from src.posts.application.use_cases import (
    CreatePostUseCase,
    DeletePostUseCase,
    GetPostsByUserUseCase,
    GetPostUseCase,
)
from src.posts.infrastructure.factory import PostFactory
from tests.posts.doubles import InMemoryUserGateway


class TestPostFactory:
    def test_create_use_cases(self, db_session: Session) -> None:
        factory = PostFactory(session=db_session, user_gateway=InMemoryUserGateway())

        assert isinstance(factory.create_create_post_use_case(), CreatePostUseCase)
        assert isinstance(factory.create_get_post_use_case(), GetPostUseCase)
        assert isinstance(factory.create_get_posts_by_user_use_case(), GetPostsByUserUseCase)
        assert isinstance(factory.create_delete_post_use_case(), DeletePostUseCase)
