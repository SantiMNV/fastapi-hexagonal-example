from src.shared.infrastructure.settings import Settings, get_settings


class TestSettings:
    def test_defaults_when_constructed_with_explicit_values(self) -> None:
        settings = Settings(
            app_name="Test App",
            database_url="sqlite:///:memory:",
            db_echo=True,
        )

        assert settings.app_name == "Test App"
        assert settings.database_url == "sqlite:///:memory:"
        assert settings.db_echo is True
        assert settings.post_service_external is False
        assert settings.posts_service_base_url == "http://localhost:8001"

    def test_get_settings_is_cached(self) -> None:
        first = get_settings()
        second = get_settings()

        assert first is second
