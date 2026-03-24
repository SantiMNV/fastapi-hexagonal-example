from sqlalchemy.orm import Session

from src.posts.infrastructure.persistence.repository import SQLAlchemyPostRepository
from src.users.application.use_cases import (
    DeleteUserUseCase,
    GetUserUseCase,
    GetUserWithPostsUseCase,
    RegisterUserUseCase,
)
from src.users.infrastructure.http.factory import UserFactory


class TestUserFactory:
    def test_create_use_cases(self, db_session: Session) -> None:
        factory = UserFactory(
            session=db_session,
            post_repository=SQLAlchemyPostRepository(db_session),
        )

        assert isinstance(factory.create_register_user_use_case(), RegisterUserUseCase)
        assert isinstance(factory.create_get_user_use_case(), GetUserUseCase)
        assert isinstance(factory.create_delete_user_use_case(), DeleteUserUseCase)
        assert isinstance(
            factory.create_get_user_with_posts_use_case(),
            GetUserWithPostsUseCase,
        )
