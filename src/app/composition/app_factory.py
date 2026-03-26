from __future__ import annotations

from datetime import timedelta

from sqlalchemy.orm import Session

from src.app.composition.gateways import build_post_gateway, build_user_gateway
from src.posts.application.ports.user_gateway import IUserGateway
from src.posts.infrastructure.factory import PostFactory
from src.shared.infrastructure.settings import Settings, get_settings
from src.users.application.ports.post_gateway import IPostGateway
from src.users.infrastructure.factory import UserFactory


class AppFactory:
    """Per-request composition root: wires factories and gateways from settings."""

    def __init__(self, *, session: Session, settings: Settings | None = None) -> None:
        self._session = session
        self._settings = settings if settings is not None else get_settings()
        self._min_account_age = timedelta(
            hours=self._settings.min_account_age_before_posting_hours,
        )
        self._user_gateway: IUserGateway | None = None
        self._post_gateway: IPostGateway | None = None
        self._posts: PostFactory | None = None
        self._users: UserFactory | None = None

    def _ensure_user_gateway(self) -> IUserGateway:
        if self._user_gateway is None:
            self._user_gateway = build_user_gateway(
                self._session,
                self._settings,
                min_account_age=self._min_account_age,
            )
        return self._user_gateway

    def _ensure_post_gateway(self) -> IPostGateway:
        if self._post_gateway is None:
            self._post_gateway = build_post_gateway(self._session, self._settings)
        return self._post_gateway

    @property
    def posts(self) -> PostFactory:
        if self._posts is None:
            self._posts = PostFactory(
                session=self._session,
                user_gateway=self._ensure_user_gateway(),
            )
        return self._posts

    @property
    def users(self) -> UserFactory:
        if self._users is None:
            self._users = UserFactory(
                session=self._session,
                post_gateway=self._ensure_post_gateway(),
                min_account_age=self._min_account_age,
            )
        return self._users
