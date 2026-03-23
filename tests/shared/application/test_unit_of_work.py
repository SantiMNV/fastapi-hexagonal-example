from sqlalchemy.orm import Session

from src.shared.application.ports.unit_of_work import UnitOfWork
from src.shared.infrastructure.persistence.unit_of_work import SQLAlchemyUnitOfWork


class TestUnitOfWorkPort:
    """Production implementation must satisfy `UnitOfWork` (structural typing)."""

    def test_sqlalchemy_unit_of_work_fulfills_port(self, db_session: Session) -> None:
        uow: UnitOfWork = SQLAlchemyUnitOfWork(db_session)

        uow.commit()
        uow.rollback()
