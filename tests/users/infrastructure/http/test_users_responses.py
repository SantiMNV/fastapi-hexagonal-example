from datetime import UTC, datetime
from uuid import uuid4

from src.posts.domain.post import Post
from src.posts.infrastructure.http.responses import PostResponse
from src.users.domain.user import User
from src.users.infrastructure.http.responses import UserResponse, UserWithPostsResponse


class TestUserResponse:
    def test_model_validate_from_domain_user(self) -> None:
        user = User(
            id=str(uuid4()),
            name="Carl",
            email="carl@example.com",
            created_at=datetime.now(UTC),
        )

        response = UserResponse.model_validate(user)

        assert response.id == user.id
        assert response.name == user.name
        assert str(response.email) == user.email
        assert response.created_at == user.created_at


class TestUserWithPostsResponse:
    def test_nested_user_and_posts(self) -> None:
        user = User(
            id=str(uuid4()),
            name="Carl",
            email="carl@example.com",
            created_at=datetime.now(UTC),
        )
        post = Post(
            id=str(uuid4()),
            user_id=user.id,
            title="T",
            content="C",
            created_at=datetime.now(UTC),
        )

        payload = UserWithPostsResponse(
            user=UserResponse.model_validate(user),
            posts=[],
        )
        assert payload.user.id == user.id

        full = UserWithPostsResponse(
            user=UserResponse.model_validate(user),
            posts=[PostResponse.model_validate(post)],
        )
        assert len(full.posts) == 1
        assert full.posts[0].title == "T"
