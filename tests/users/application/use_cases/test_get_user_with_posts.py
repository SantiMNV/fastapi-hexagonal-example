from datetime import UTC, datetime
from uuid import uuid4

import pytest

from src.posts.domain.post import Post
from src.users.application.use_cases.get_user_with_posts import GetUserWithPostsUseCase
from src.users.domain.exceptions import UserNotFoundException
from tests.users.doubles import (
    InMemoryPostRepository,
    InMemoryUserRepository,
    sample_user,
)


class TestGetUserWithPostsUseCase:
    async def test_returns_user_and_posts(self) -> None:
        users = InMemoryUserRepository()
        posts = InMemoryPostRepository()
        user = sample_user()
        await users.add(user)
        post = Post(
            id=str(uuid4()),
            user_id=user.id,
            title="Hi",
            content="Body",
            created_at=datetime.now(UTC),
        )
        await posts.add(post)
        use_case = GetUserWithPostsUseCase(users, posts)

        u, user_posts = await use_case.execute(user.id)

        assert u is user
        assert len(user_posts) == 1
        assert user_posts[0] is post

    async def test_raises_when_user_missing(self) -> None:
        use_case = GetUserWithPostsUseCase(InMemoryUserRepository(), InMemoryPostRepository())

        with pytest.raises(UserNotFoundException):
            await use_case.execute("missing-id")
