from __future__ import annotations

from datetime import UTC, datetime, timedelta

from src.users.application.ports.user_repository import IUserRepository
from src.users.domain.exceptions import UserCannotCreatePostsYetException, UserNotFoundException


class VerifyUserCanCreatePostUseCase:
    """Users-context policy invoked when another BC needs to author content as this user."""

    def __init__(
        self,
        repository: IUserRepository,
        *,
        min_account_age: timedelta = timedelta(hours=24),
    ) -> None:
        self._repository = repository
        self._min_account_age = min_account_age

    async def execute(self, user_id: str, *, now: datetime | None = None) -> None:
        now = now if now is not None else datetime.now(UTC)
        user = await self._repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundException(user_id)
        if not user.can_create_posts(now=now, min_account_age=self._min_account_age):
            raise UserCannotCreatePostsYetException(user_id)
