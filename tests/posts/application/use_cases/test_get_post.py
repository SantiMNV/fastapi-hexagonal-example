import pytest

from src.posts.application.use_cases.get_post import GetPostUseCase
from src.posts.domain.exceptions import PostNotFoundException
from tests.posts.doubles import InMemoryPostRepository, sample_post, sample_user


class TestGetPostUseCase:
    async def test_returns_post(self) -> None:
        posts = InMemoryPostRepository()
        user = sample_user()
        post = sample_post(user_id=user.id)
        await posts.add(post)
        use_case = GetPostUseCase(posts)

        result = await use_case.execute(post.id)

        assert result is post

    async def test_raises_when_missing(self) -> None:
        use_case = GetPostUseCase(InMemoryPostRepository())

        with pytest.raises(PostNotFoundException):
            await use_case.execute("missing-id")
