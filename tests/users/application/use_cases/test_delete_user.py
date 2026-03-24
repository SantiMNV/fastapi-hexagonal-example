import pytest

from src.users.application.use_cases.delete_user import DeleteUserUseCase
from src.users.domain.exceptions import UserNotFoundException
from tests.users.doubles import InMemoryUserRepository, NoOpUnitOfWork, sample_user


class TestDeleteUserUseCase:
    async def test_removes_user(self) -> None:
        repository = InMemoryUserRepository()
        user = sample_user()
        await repository.add(user)
        use_case = DeleteUserUseCase(repository, NoOpUnitOfWork())

        await use_case.execute(user.id)

        assert await repository.get_by_id(user.id) is None

    async def test_raises_when_missing(self) -> None:
        use_case = DeleteUserUseCase(InMemoryUserRepository(), NoOpUnitOfWork())

        with pytest.raises(UserNotFoundException):
            await use_case.execute("missing-id")
