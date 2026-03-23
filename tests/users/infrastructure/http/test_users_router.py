from fastapi.testclient import TestClient


class TestUsersRouter:
    def _register(self, client: TestClient, *, email: str = "user@example.com") -> str:
        response = client.post("/users", json={"name": "Test User", "email": email})
        assert response.status_code == 201
        return response.json()["id"]

    def test_register_returns_user(self, client: TestClient) -> None:
        response = client.post("/users", json={"name": "Ada", "email": "ada@example.com"})

        assert response.status_code == 201
        body = response.json()
        assert body["name"] == "Ada"
        assert body["email"] == "ada@example.com"
        assert body["id"]

    def test_register_conflict_returns_409(self, client: TestClient) -> None:
        self._register(client, email="dup@example.com")
        response = client.post("/users", json={"name": "Other", "email": "dup@example.com"})

        assert response.status_code == 409

    def test_get_user_returns_404_when_missing(self, client: TestClient) -> None:
        response = client.get("/users/00000000-0000-0000-0000-000000000000")

        assert response.status_code == 404

    def test_get_user_after_register(self, client: TestClient) -> None:
        user_id = self._register(client, email="get@example.com")

        response = client.get(f"/users/{user_id}")

        assert response.status_code == 200
        assert response.json()["email"] == "get@example.com"

    def test_delete_user_returns_204(self, client: TestClient) -> None:
        user_id = self._register(client, email="del@example.com")

        response = client.delete(f"/users/{user_id}")

        assert response.status_code == 204
        assert client.get(f"/users/{user_id}").status_code == 404

    def test_delete_missing_returns_404(self, client: TestClient) -> None:
        response = client.delete("/users/00000000-0000-0000-0000-000000000099")

        assert response.status_code == 404

    def test_list_posts_for_user_empty(self, client: TestClient) -> None:
        user_id = self._register(client, email="noposts@example.com")

        response = client.get(f"/users/{user_id}/posts")

        assert response.status_code == 200
        assert response.json() == []

    def test_with_posts_empty(self, client: TestClient) -> None:
        user_id = self._register(client, email="withposts@example.com")

        response = client.get(f"/users/{user_id}/with-posts")

        assert response.status_code == 200
        body = response.json()
        assert body["user"]["id"] == user_id
        assert body["posts"] == []

    def test_with_posts_includes_created_post(
        self, client: TestClient, posts_client: TestClient
    ) -> None:
        user_id = self._register(client, email="author@example.com")
        post = posts_client.post(
            "/posts",
            json={"user_id": user_id, "title": "Hello", "content": "World"},
        )
        assert post.status_code == 201

        response = client.get(f"/users/{user_id}/with-posts")

        assert response.status_code == 200
        posts = response.json()["posts"]
        assert len(posts) == 1
        assert posts[0]["title"] == "Hello"
