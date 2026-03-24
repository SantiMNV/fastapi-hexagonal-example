import pytest

from src.posts.application.use_cases.list_user_posts import ListUserPostsUseCase
from src.posts.domain.exceptions import PostAuthorNotFoundException
from tests.posts.doubles import (
    InMemoryPostRepository,
    InMemoryUserRepository,
    sample_post,
    sample_user,
)


class TestListUserPostsUseCase:
    async def test_returns_posts_for_user(self) -> None:
        users = InMemoryUserRepository()
        posts = InMemoryPostRepository()
        user = sample_user()
        await users.add(user)
        p1 = sample_post(user_id=user.id)
        await posts.add(p1)
        use_case = ListUserPostsUseCase(posts, users)

        result = await use_case.execute(user.id)

        assert result == [p1]

    async def test_raises_when_author_missing(self) -> None:
        use_case = ListUserPostsUseCase(InMemoryPostRepository(), InMemoryUserRepository())

        with pytest.raises(PostAuthorNotFoundException):
            await use_case.execute("missing-user")
