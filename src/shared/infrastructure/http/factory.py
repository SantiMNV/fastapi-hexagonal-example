from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Session

from src.posts.application.ports.user_gateway import IUserGateway
from src.shared.infrastructure.settings import get_settings
from src.users.application.ports.post_gateway import IPostGateway

if TYPE_CHECKING:
    from src.posts.infrastructure.http.factory import PostFactory
    from src.users.infrastructure.http.factory import UserFactory


class _NoCommitUnitOfWork:
    """No-op UoW used in the monolith so that a gateway's inner use case does not
    commit mid-transaction — the outer use case owns the session commit."""

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


class AppFactory:
    """Per-request composition root: wires factories and gateways from settings."""

    def __init__(self, *, session: Session) -> None:
        self._session = session
        self._settings = get_settings()
        self._posts: PostFactory | None = None
        self._users: UserFactory | None = None

    @property
    def posts(self) -> PostFactory:
        if self._posts is None:
            from src.posts.infrastructure.http.factory import PostFactory

            self._posts = PostFactory(
                session=self._session,
                user_gateway=self._make_user_gateway(),
            )
        return self._posts

    @property
    def users(self) -> UserFactory:
        if self._users is None:
            from src.users.infrastructure.http.factory import UserFactory

            self._users = UserFactory(
                session=self._session, post_gateway=self._make_post_gateway()
            )
        return self._users

    def _make_user_gateway(self) -> IUserGateway:
        if self._settings.users_service_url is None:
            from src.posts.infrastructure.persistence.local_user_gateway import (
                LocalUserGateway,
            )
            from src.users.application.use_cases.get_user import GetUserUseCase
            from src.users.infrastructure.persistence.repository import (
                SQLAlchemyUserRepository,
            )

            get_user = GetUserUseCase(SQLAlchemyUserRepository(self._session))
            return LocalUserGateway(get_user)
        if not self._settings.internal_api_key:
            raise ValueError(
                "internal_api_key is required when users_service_url is set (remote user gateway)",
            )
        from src.posts.infrastructure.http.http_user_gateway import HttpUserGateway

        return HttpUserGateway(
            self._settings.users_service_url,
            internal_api_key=self._settings.internal_api_key,
            internal_api_header_name=self._settings.internal_api_header_name,
        )

    def _make_post_gateway(self) -> IPostGateway:
        if self._settings.posts_service_url is None:
            from src.posts.application.use_cases.delete_user_posts import (
                DeleteUserPostsUseCase,
            )
            from src.posts.application.use_cases.get_posts_by_user import (
                GetPostsByUserUseCase,
            )
            from src.posts.infrastructure.persistence.repository import (
                SQLAlchemyPostRepository,
            )
            from src.users.infrastructure.persistence.local_post_gateway import (
                LocalPostGateway,
            )

            post_repo = SQLAlchemyPostRepository(self._session)
            list_uc = GetPostsByUserUseCase(post_repo)
            delete_uc = DeleteUserPostsUseCase(post_repo, _NoCommitUnitOfWork())
            return LocalPostGateway(list_uc, delete_uc)
        if not self._settings.internal_api_key:
            raise ValueError(
                "internal_api_key is required when posts_service_url is set (remote post gateway)",
            )
        from src.users.infrastructure.http.http_post_gateway import HttpPostGateway

        return HttpPostGateway(
            self._settings.posts_service_url,
            internal_api_key=self._settings.internal_api_key,
            internal_api_header_name=self._settings.internal_api_header_name,
        )
