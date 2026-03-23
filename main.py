from contextlib import asynccontextmanager
from typing import Callable
import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.shared.infrastructure.persistence.orm import create_tables
from src.shared.infrastructure.settings import Settings, get_settings
from src.users.infrastructure.http.router import router as users_router


def _open_posts_bridge(settings: Settings) -> tuple[httpx.Client, Callable | None]:
    """Returns (client, closer) where closer is a context manager exit or None to call .close()."""
    if settings.posts_service_base_url == "__embedded_posts__":
        from posts_main import create_posts_app

        posts_app = create_posts_app()
        test_client = TestClient(posts_app)
        return test_client.__enter__(), test_client.__exit__
    client = httpx.Client(
        base_url=settings.posts_service_base_url.rstrip("/"),
        timeout=10.0,
    )
    return client, None


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    engine = create_engine(settings.database_url, echo=settings.db_echo)
    create_tables(engine)
    app.state.session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )
    bridge, closer = _open_posts_bridge(settings)
    app.state.posts_bridge = bridge
    try:
        yield
    finally:
        if closer is not None:
            closer()
        else:
            bridge.close()
        engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(title="FastAPI Hexagonal Example (users)", lifespan=lifespan)
    app.include_router(users_router)
    return app


app = create_app()
