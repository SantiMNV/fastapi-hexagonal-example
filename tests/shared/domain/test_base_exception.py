from src.shared.domain.base_exception import BaseAppException


class TestBaseAppException:
    def test_stores_message_and_default_code(self) -> None:
        exc = BaseAppException("oops")

        assert exc.message == "oops"
        assert exc.code == "application_error"
        assert str(exc) == "oops"

    def test_accepts_custom_code(self) -> None:
        exc = BaseAppException("nope", code="custom")

        assert exc.code == "custom"
