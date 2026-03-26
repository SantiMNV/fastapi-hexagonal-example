from datetime import UTC, datetime, timedelta

import pytest

from src.users.application.use_cases.verify_user_can_create_post import (
    VerifyUserCanCreatePostUseCase,
)
from src.users.domain.exceptions import UserCannotCreatePostsYetException, UserNotFoundException
from tests.users.doubles import InMemoryUserRepository, sample_user


class TestVerifyUserCanCreatePostUseCase:
    async def test_allows_when_account_old_enough(self) -> None:
        repo = InMemoryUserRepository()
        user = sample_user()
        user.created_at = datetime.now(UTC) - timedelta(days=2)
        await repo.add(user)
        use_case = VerifyUserCanCreatePostUseCase(repo, min_account_age=timedelta(hours=24))

        await use_case.execute(user.id)

    async def test_rejects_missing_user(self) -> None:
        use_case = VerifyUserCanCreatePostUseCase(
            InMemoryUserRepository(), min_account_age=timedelta(hours=24)
        )

        with pytest.raises(UserNotFoundException):
            await use_case.execute("missing")

    async def test_rejects_too_new_account(self) -> None:
        repo = InMemoryUserRepository()
        user = sample_user()
        user.created_at = datetime.now(UTC) - timedelta(hours=1)
        await repo.add(user)
        use_case = VerifyUserCanCreatePostUseCase(repo, min_account_age=timedelta(hours=24))

        with pytest.raises(UserCannotCreatePostsYetException):
            await use_case.execute(user.id)
