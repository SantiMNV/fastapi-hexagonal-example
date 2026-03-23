from datetime import UTC, datetime
from uuid import uuid4

from src.users.domain.user import User


class TestUser:
    def test_dataclass_fields(self) -> None:
        uid = str(uuid4())
        created = datetime.now(UTC)
        user = User(id=uid, name="Bob", email="bob@example.com", created_at=created)

        assert user.id == uid
        assert user.name == "Bob"
        assert user.email == "bob@example.com"
        assert user.created_at is created
