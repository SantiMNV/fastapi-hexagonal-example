from src.posts.domain.exceptions import PostNotFoundException


class TestPostExceptions:
    def test_post_not_found_message_and_code(self) -> None:
        exc = PostNotFoundException("p-1")

        assert "p-1" in exc.message
        assert exc.code == "post_not_found"
