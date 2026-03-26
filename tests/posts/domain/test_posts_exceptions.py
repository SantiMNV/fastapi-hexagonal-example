from src.posts.domain.exceptions import PostAuthorNotEligibleException, PostNotFoundException


class TestPostExceptions:
    def test_post_not_found_message_and_code(self) -> None:
        exc = PostNotFoundException("p-1")

        assert "p-1" in exc.message
        assert exc.code == "post_not_found"

    def test_post_author_not_eligible_code(self) -> None:
        exc = PostAuthorNotEligibleException("u-1")

        assert exc.code == "post_author_not_eligible"
