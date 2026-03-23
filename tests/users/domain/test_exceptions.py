from src.users.domain.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)


class TestUserExceptions:
    def test_user_not_found_message_and_code(self) -> None:
        exc = UserNotFoundException("u-1")

        assert "u-1" in exc.message
        assert exc.code == "user_not_found"

    def test_user_already_exists_message_and_code(self) -> None:
        exc = UserAlreadyExistsException("dup@example.com")

        assert "dup@example.com" in exc.message
        assert exc.code == "user_already_exists"

    def test_subclass_base_app_exception(self) -> None:
        assert isinstance(UserNotFoundException("x"), Exception)
        assert isinstance(UserAlreadyExistsException("a@b.c"), Exception)
