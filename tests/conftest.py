from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.shared.infrastructure.persistence.orm import create_tables
from src.shared.infrastructure.settings import get_settings
from src.shared.main import create_app


@pytest.fixture(autouse=True)
def reset_get_settings_cache() -> Generator[None]:
    get_settings.cache_clear()
    yield None
    get_settings.cache_clear()


@pytest.fixture
def database_url(tmp_path) -> str:
    # File-based SQLite so all connections (lifespan engine + request sessions) share one DB.
    return f"sqlite:///{(tmp_path / 'app.db').resolve().as_posix()}"


@pytest.fixture
def sqlite_engine(database_url: str):
    engine = create_engine(database_url)
    create_tables(engine)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def session_factory(sqlite_engine):
    return sessionmaker(bind=sqlite_engine, autoflush=False, autocommit=False)


@pytest.fixture
def db_session(session_factory) -> Generator[Session]:
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def app(monkeypatch, database_url: str):
    monkeypatch.setenv("DATABASE_URL", database_url)
    # Register /internal/* routes and match outbound S2S client expectations in tests.
    monkeypatch.setenv("INTERNAL_API_KEY", "test-internal-api-key")
    return create_app()


@pytest.fixture
def client(app):
    with TestClient(app) as test_client:
        yield test_client
