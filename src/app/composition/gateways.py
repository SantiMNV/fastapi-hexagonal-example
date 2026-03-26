from __future__ import annotations

from datetime import timedelta

from sqlalchemy.orm import Session

from src.posts.application.ports.user_gateway import IUserGateway
from src.posts.application.use_cases import DeleteUserPostsUseCase, GetPostsByUserUseCase
from src.posts.infrastructure.http.http_user_gateway import HttpUserGateway
from src.posts.infrastructure.persistence.local_user_gateway import LocalUserGateway
from src.posts.infrastructure.persistence.repository import SQLAlchemyPostRepository
from src.shared.infrastructure.persistence.unit_of_work import NoOpUnitOfWork
from src.shared.infrastructure.settings import Settings
from src.users.application.ports.post_gateway import IPostGateway
from src.users.application.use_cases.get_user import GetUserUseCase
from src.users.application.use_cases.verify_user_can_create_post import (
    VerifyUserCanCreatePostUseCase,
)
from src.users.infrastructure.http.http_post_gateway import HttpPostGateway
from src.users.infrastructure.persistence.local_post_gateway import LocalPostGateway
from src.users.infrastructure.persistence.repository import SQLAlchemyUserRepository


def build_user_gateway(
    session: Session,
    settings: Settings,
    *,
    min_account_age: timedelta,
) -> IUserGateway:
    if settings.users_service_url is None:
        user_repo = SQLAlchemyUserRepository(session)
        verify = VerifyUserCanCreatePostUseCase(user_repo, min_account_age=min_account_age)
        get_user = GetUserUseCase(user_repo)
        return LocalUserGateway(get_user, verify)
    if not settings.internal_api_key:
        msg = "internal_api_key is required when users_service_url is set (remote user gateway)"
        raise ValueError(msg)
    return HttpUserGateway(
        settings.users_service_url,
        internal_api_key=settings.internal_api_key,
        internal_api_header_name=settings.internal_api_header_name,
    )


def build_post_gateway(session: Session, settings: Settings) -> IPostGateway:
    if settings.posts_service_url is None:
        post_repo = SQLAlchemyPostRepository(session)
        list_uc = GetPostsByUserUseCase(post_repo)
        delete_uc = DeleteUserPostsUseCase(post_repo, NoOpUnitOfWork())
        return LocalPostGateway(list_uc, delete_uc)
    if not settings.internal_api_key:
        msg = "internal_api_key is required when posts_service_url is set (remote post gateway)"
        raise ValueError(msg)
    return HttpPostGateway(
        settings.posts_service_url,
        internal_api_key=settings.internal_api_key,
        internal_api_header_name=settings.internal_api_header_name,
    )
