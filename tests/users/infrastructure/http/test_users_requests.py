import pytest
from pydantic import ValidationError

from src.users.infrastructure.http.requests import RegisterUserRequest


class TestRegisterUserRequest:
    def test_accepts_valid_email(self) -> None:
        body = RegisterUserRequest(name="Ann", email="ann@example.com")

        assert body.name == "Ann"
        assert str(body.email) == "ann@example.com"

    def test_rejects_invalid_email(self) -> None:
        with pytest.raises(ValidationError):
            RegisterUserRequest(name="Ann", email="not-an-email")
