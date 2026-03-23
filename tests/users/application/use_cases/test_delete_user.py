import pytest

from src.users.application.use_cases.delete_user import DeleteUserUseCase
from src.users.domain.exceptions import UserNotFoundException
from tests.users.doubles import InMemoryUserRepository, NoOpUnitOfWork, sample_user


class TestDeleteUserUseCase:
    def test_removes_user(self) -> None:
        repository = InMemoryUserRepository()
        user = sample_user()
        repository.add(user)
        use_case = DeleteUserUseCase(repository, NoOpUnitOfWork())

        use_case.execute(user.id)

        assert repository.get_by_id(user.id) is None

    def test_raises_when_missing(self) -> None:
        use_case = DeleteUserUseCase(InMemoryUserRepository(), NoOpUnitOfWork())

        with pytest.raises(UserNotFoundException):
            use_case.execute("missing-id")
