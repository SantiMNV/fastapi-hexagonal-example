from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.posts.infrastructure.http.internal_router import router as posts_internal_router
from src.posts.infrastructure.http.router import router as posts_router
from src.shared.infrastructure.persistence.orm import create_tables
from src.shared.infrastructure.settings import get_settings
from src.users.infrastructure.http.internal_router import router as users_internal_router
from src.users.infrastructure.http.router import router as users_router


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
    try:
        yield
    finally:
        engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(title="FastAPI Hexagonal Example", lifespan=lifespan)
    app.include_router(users_router)
    app.include_router(posts_router)
    settings = get_settings()
    if settings.internal_api_key:
        app.include_router(posts_internal_router)
        app.include_router(users_internal_router)
    return app


app = create_app()
