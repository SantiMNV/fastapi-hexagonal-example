from sqlalchemy.orm import Session

from src.posts.application.ports.post_repository import PostRepository
from src.posts.infrastructure.persistence.repository import SQLAlchemyPostRepository


class TestPostRepositoryPort:
    def test_sqlalchemy_repository_fulfills_port(self, db_session: Session) -> None:
        repository: PostRepository = SQLAlchemyPostRepository(db_session)

        assert repository.get_by_id("nonexistent") is None
