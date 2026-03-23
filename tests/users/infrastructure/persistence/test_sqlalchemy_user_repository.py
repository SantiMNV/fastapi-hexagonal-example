from sqlalchemy.orm import Session

from src.users.infrastructure.persistence.repository import SQLAlchemyUserRepository
from tests.users.doubles import sample_user


class TestSQLAlchemyUserRepository:
    def test_add_get_by_id_and_email(self, db_session: Session) -> None:
        repo = SQLAlchemyUserRepository(db_session)
        user = sample_user(email="repo@example.com")

        repo.add(user)
        db_session.flush()

        by_id = repo.get_by_id(user.id)
        by_email = repo.get_by_email("repo@example.com")
        assert by_id is not None and by_email is not None
        assert by_id.id == user.id == by_email.id
        assert by_id.email == user.email
        assert by_id.name == user.name

    def test_get_by_id_returns_none_when_missing(self, db_session: Session) -> None:
        repo = SQLAlchemyUserRepository(db_session)

        assert repo.get_by_id("missing") is None

    def test_delete_removes_row(self, db_session: Session) -> None:
        repo = SQLAlchemyUserRepository(db_session)
        user = sample_user()
        repo.add(user)
        db_session.flush()

        repo.delete(user.id)
        db_session.flush()

        assert repo.get_by_id(user.id) is None

    def test_delete_is_noop_when_row_missing(self, db_session: Session) -> None:
        repo = SQLAlchemyUserRepository(db_session)

        repo.delete("does-not-exist")

        assert repo.get_by_id("does-not-exist") is None
