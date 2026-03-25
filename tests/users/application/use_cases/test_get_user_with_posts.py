from datetime import UTC, datetime
from uuid import uuid4

import pytest

from src.posts.domain.post import Post
from src.users.application.use_cases.get_user_with_posts import GetUserWithPostsUseCase
from src.users.domain.exceptions import UserNotFoundException
from tests.users.doubles import (
    InMemoryPostGateway,
    InMemoryPostRepository,
    InMemoryUserRepository,
    sample_user,
)


class TestGetUserWithPostsUseCase:
    async def test_returns_user_and_posts(self) -> None:
        users = InMemoryUserRepository()
        posts_repo = InMemoryPostRepository()
        post_gateway = InMemoryPostGateway(posts_repo)
        user = sample_user()
        await users.add(user)
        post = Post(
            id=str(uuid4()),
            user_id=user.id,
            title="Hi",
            content="Body",
            created_at=datetime.now(UTC),
        )
        await posts_repo.add(post)
        use_case = GetUserWithPostsUseCase(users, post_gateway)

        u, user_posts = await use_case.execute(user.id)

        assert u is user
        assert len(user_posts) == 1
        assert user_posts[0].id == post.id
        assert user_posts[0].title == post.title

    async def test_raises_when_user_missing(self) -> None:
        use_case = GetUserWithPostsUseCase(InMemoryUserRepository(), InMemoryPostGateway())

        with pytest.raises(UserNotFoundException):
            await use_case.execute("missing-id")
