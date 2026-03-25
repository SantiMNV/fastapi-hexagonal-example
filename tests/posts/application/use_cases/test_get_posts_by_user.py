from src.posts.application.use_cases.get_posts_by_user import GetPostsByUserUseCase
from tests.posts.doubles import InMemoryPostRepository, sample_post


class TestGetPostsByUserUseCase:
    async def test_returns_posts_for_user(self) -> None:
        posts = InMemoryPostRepository()
        user_id = "some-user"
        p1 = sample_post(user_id=user_id)
        await posts.add(p1)
        use_case = GetPostsByUserUseCase(posts)

        result = await use_case.execute(user_id)

        assert result == [p1]

    async def test_returns_empty_for_unknown_user(self) -> None:
        use_case = GetPostsByUserUseCase(InMemoryPostRepository())

        result = await use_case.execute("unknown-user")

        assert result == []
