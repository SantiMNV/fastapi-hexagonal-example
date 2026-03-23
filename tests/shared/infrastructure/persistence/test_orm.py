from sqlalchemy import create_engine

from src.shared.infrastructure.persistence.orm import Base, create_tables


class TestSharedPersistenceOrm:
    def test_create_tables_registers_user_and_post_tables(self) -> None:
        engine = create_engine("sqlite:///:memory:")
        create_tables(engine)

        table_names = set(Base.metadata.tables.keys())

        assert "users" in table_names
        assert "posts" in table_names
        engine.dispose()
