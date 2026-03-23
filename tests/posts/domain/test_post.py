from datetime import UTC, datetime
from uuid import uuid4

from src.posts.domain.post import Post


class TestPost:
    def test_dataclass_fields(self) -> None:
        pid = str(uuid4())
        uid = str(uuid4())
        created = datetime.now(UTC)
        post = Post(
            id=pid,
            user_id=uid,
            title="T",
            content="C",
            created_at=created,
        )

        assert post.id == pid
        assert post.user_id == uid
        assert post.title == "T"
        assert post.content == "C"
        assert post.created_at is created
