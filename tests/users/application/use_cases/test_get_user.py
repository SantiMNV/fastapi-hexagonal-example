import pytest

from src.users.application.use_cases.get_user import GetUserUseCase
from src.users.domain.exceptions import UserNotFoundException
from tests.users.doubles import InMemoryUserRepository, sample_user


class TestGetUserUseCase:
    async def test_returns_user(self) -> None:
        repository = InMemoryUserRepository()
        user = sample_user()
        await repository.add(user)
        use_case = GetUserUseCase(repository)

        result = await use_case.execute(user.id)

        assert result is user

    async def test_raises_when_missing(self) -> None:
        use_case = GetUserUseCase(InMemoryUserRepository())

        with pytest.raises(UserNotFoundException):
            await use_case.execute("missing-id")
