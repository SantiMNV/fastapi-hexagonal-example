from sqlalchemy.orm import Session


class SQLAlchemyUnitOfWork:
    __slots__ = ("_session",)

    def __init__(self, session: Session) -> None:
        self._session = session

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
