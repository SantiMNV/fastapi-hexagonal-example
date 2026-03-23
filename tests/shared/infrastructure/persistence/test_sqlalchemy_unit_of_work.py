from sqlalchemy.orm import Session

from src.shared.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork


class TestSQLAlchemyUnitOfWork:
    def test_commit_and_rollback(self, db_session: Session) -> None:
        uow = SQLAlchemyUnitOfWork(db_session)

        uow.commit()
        uow.rollback()
