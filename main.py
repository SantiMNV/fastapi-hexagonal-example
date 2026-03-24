from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.posts.infrastructure.http.router import router as posts_router
from src.shared.infrastructure.http.client import create_shared_async_client
from src.shared.infrastructure.persistence.orm import create_tables
from src.shared.infrastructure.settings import get_settings
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
    if settings.post_service_external:
        app.state.posts_http_client = create_shared_async_client()
    try:
        yield
    finally:
        if settings.post_service_external:
            await app.state.posts_http_client.aclose()
        engine.dispose()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    app.include_router(users_router)
    if not settings.post_service_external:
        app.include_router(posts_router)
    return app


app = create_app()
