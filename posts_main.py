"""Posts-only FastAPI app (separate process / container; same DATABASE_URL as users)."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.posts.infrastructure.http.router import router as posts_router
from src.shared.infrastructure.persistence.orm import create_tables
from src.shared.infrastructure.settings import get_settings


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


def create_posts_app() -> FastAPI:
    app = FastAPI(title="Posts service", lifespan=lifespan)
    app.include_router(posts_router)
    return app


app = create_posts_app()
