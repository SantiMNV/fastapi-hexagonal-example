import pytest

from src.posts.application.use_cases.delete_post import DeletePostUseCase
from src.posts.domain.exceptions import PostNotFoundException
from tests.posts.doubles import InMemoryPostRepository, NoOpUnitOfWork, sample_post, sample_user


class TestDeletePostUseCase:
    def test_removes_post(self) -> None:
        posts = InMemoryPostRepository()
        user = sample_user()
        post = sample_post(user_id=user.id)
        posts.add(post)
        use_case = DeletePostUseCase(posts, NoOpUnitOfWork())

        use_case.execute(post.id)

        assert posts.get_by_id(post.id) is None

    def test_raises_when_missing(self) -> None:
        use_case = DeletePostUseCase(InMemoryPostRepository(), NoOpUnitOfWork())

        with pytest.raises(PostNotFoundException):
            use_case.execute("missing-id")
