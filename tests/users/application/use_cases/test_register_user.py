import pytest

from src.users.application.use_cases.register_user import RegisterUserUseCase
from src.users.domain.exceptions import UserAlreadyExistsException
from tests.users.doubles import InMemoryUserRepository, NoOpUnitOfWork


class TestRegisterUserUseCase:
    def test_creates_user(self) -> None:
        repository = InMemoryUserRepository()
        use_case = RegisterUserUseCase(repository, NoOpUnitOfWork())

        user = use_case.execute(name="Alice", email="alice@example.com")

        assert user.id
        assert repository.get_by_email("alice@example.com") is not None

    def test_raises_if_email_already_exists(self) -> None:
        repository = InMemoryUserRepository()
        use_case = RegisterUserUseCase(repository, NoOpUnitOfWork())

        use_case.execute(name="Alice", email="alice@example.com")

        with pytest.raises(UserAlreadyExistsException):
            use_case.execute(name="Another", email="alice@example.com")
