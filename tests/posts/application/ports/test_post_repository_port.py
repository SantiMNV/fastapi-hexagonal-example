from sqlalchemy.orm import Session

from src.posts.application.ports.post_repository import IPostRepository
from src.posts.infrastructure.persistence.repository import SQLAlchemyPostRepository


class TestPostRepositoryPort:
    async def test_sqlalchemy_repository_fulfills_port(self, db_session: Session) -> None:
        repository: IPostRepository = SQLAlchemyPostRepository(db_session)

        assert await repository.get_by_id("nonexistent") is None
