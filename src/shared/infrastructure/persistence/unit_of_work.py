from sqlalchemy.orm import Session

from src.shared.application.ports.unit_of_work import UnitOfWork


class NoOpUnitOfWork:
    """No-op UoW for use cases invoked as inner operations within an existing transaction."""

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


class SQLAlchemyUnitOfWork(UnitOfWork):
    __slots__ = ("_session",)

    def __init__(self, session: Session) -> None:
        self._session = session

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
