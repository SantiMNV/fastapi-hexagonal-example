from datetime import UTC, datetime
from uuid import uuid4

from src.posts.domain.post import Post
from src.posts.infrastructure.http.responses import PostResponse


class TestPostResponse:
    def test_model_validate_from_domain_post(self) -> None:
        post = Post(
            id=str(uuid4()),
            user_id=str(uuid4()),
            title="T",
            content="C",
            created_at=datetime.now(UTC),
        )

        response = PostResponse.model_validate(post)

        assert response.id == post.id
        assert response.user_id == post.user_id
        assert response.title == post.title
        assert response.content == post.content
        assert response.created_at == post.created_at
