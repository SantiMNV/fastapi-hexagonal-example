from datetime import UTC, datetime

import pytest

from src.posts.application.use_cases.create_post import CreatePostUseCase
from src.posts.domain.exceptions import PostAuthorNotFoundException
from src.posts.domain.user_snapshot import UserSnapshot
from tests.posts.doubles import InMemoryPostRepository, InMemoryUserGateway, NoOpUnitOfWork


class TestCreatePostUseCase:
    async def test_creates_post(self) -> None:
        posts = InMemoryPostRepository()
        users = InMemoryUserGateway()
        users.snapshots["some-user"] = UserSnapshot(
            id="some-user",
            name="Author",
            email="a@example.com",
            created_at=datetime.now(UTC),
        )
        use_case = CreatePostUseCase(posts, users, NoOpUnitOfWork())

        post = await use_case.execute(user_id="some-user", title="Hi", content="Body")

        assert post.id
        assert post.user_id == "some-user"
        assert await posts.get_by_id(post.id) is post

    async def test_rejects_unknown_author(self) -> None:
        posts = InMemoryPostRepository()
        use_case = CreatePostUseCase(posts, InMemoryUserGateway(), NoOpUnitOfWork())

        with pytest.raises(PostAuthorNotFoundException):
            await use_case.execute(user_id="missing", title="Hi", content="Body")
