from sqlalchemy.orm import Session

from src.users.application.ports.user_repository import UserRepository
from src.users.infrastructure.persistence.repository import SQLAlchemyUserRepository


class TestUserRepositoryPort:
    def test_sqlalchemy_repository_fulfills_port(self, db_session: Session) -> None:
        repository: UserRepository = SQLAlchemyUserRepository(db_session)

        assert repository.get_by_id("nonexistent") is None
