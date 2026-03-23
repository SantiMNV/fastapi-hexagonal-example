from src.posts.infrastructure.http.requests import CreatePostRequest


class TestCreatePostRequest:
    def test_fields(self) -> None:
        body = CreatePostRequest(user_id="u1", title="T", content="C")

        assert body.user_id == "u1"
        assert body.title == "T"
        assert body.content == "C"
