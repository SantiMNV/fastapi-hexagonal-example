from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def create_tables(engine: Engine) -> None:
    Base.metadata.create_all(bind=engine)
