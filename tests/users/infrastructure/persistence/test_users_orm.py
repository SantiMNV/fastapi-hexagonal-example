from src.users.infrastructure.persistence.orm import UserORM


class TestUserORM:
    def test_maps_users_table(self) -> None:
        assert UserORM.__tablename__ == "users"
