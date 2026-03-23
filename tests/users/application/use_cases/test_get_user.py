import pytest

from src.users.application.use_cases.get_user import GetUserUseCase
from src.users.domain.exceptions import UserNotFoundException
from tests.users.doubles import InMemoryUserRepository, sample_user


class TestGetUserUseCase:
    def test_returns_user(self) -> None:
        repository = InMemoryUserRepository()
        user = sample_user()
        repository.add(user)
        use_case = GetUserUseCase(repository)

        result = use_case.execute(user.id)

        assert result is user

    def test_raises_when_missing(self) -> None:
        use_case = GetUserUseCase(InMemoryUserRepository())

        with pytest.raises(UserNotFoundException):
            use_case.execute("missing-id")
