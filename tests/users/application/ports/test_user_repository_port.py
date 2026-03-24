from sqlalchemy.orm import Session

from src.users.application.ports.user_repository import IUserRepository
from src.users.infrastructure.persistence.repository import SQLAlchemyUserRepository


class TestUserRepositoryPort:
    async def test_sqlalchemy_repository_fulfills_port(self, db_session: Session) -> None:
        repository: IUserRepository = SQLAlchemyUserRepository(db_session)

        assert await repository.get_by_id("nonexistent") is None
