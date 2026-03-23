import pytest

from src.posts.application.use_cases.create_post import CreatePostUseCase
from src.posts.domain.exceptions import PostAuthorNotFoundException
from tests.posts.doubles import (
    InMemoryPostRepository,
    InMemoryUserRepository,
    NoOpUnitOfWork,
    sample_user,
)


class TestCreatePostUseCase:
    def test_creates_post_when_author_exists(self) -> None:
        users = InMemoryUserRepository()
        posts = InMemoryPostRepository()
        user = sample_user()
        users.add(user)
        use_case = CreatePostUseCase(posts, users, NoOpUnitOfWork())

        post = use_case.execute(user_id=user.id, title="Hi", content="Body")

        assert post.id
        assert post.user_id == user.id
        assert posts.get_by_id(post.id) is post

    def test_raises_when_author_missing(self) -> None:
        use_case = CreatePostUseCase(
            InMemoryPostRepository(),
            InMemoryUserRepository(),
            NoOpUnitOfWork(),
        )

        with pytest.raises(PostAuthorNotFoundException):
            use_case.execute(user_id="missing-user", title="x", content="y")
