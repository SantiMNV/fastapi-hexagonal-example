from fastapi.testclient import TestClient


class TestPostsRouter:
    def _register_user(self, client: TestClient, *, email: str = "author@example.com") -> str:
        response = client.post("/users", json={"name": "Author", "email": email})
        assert response.status_code == 201
        return response.json()["id"]

    def test_create_post_returns_201(self, client: TestClient) -> None:
        user_id = self._register_user(client, email="create@example.com")

        response = client.post(
            "/posts",
            json={"user_id": user_id, "title": "Hello", "content": "World"},
        )

        assert response.status_code == 201
        body = response.json()
        assert body["user_id"] == user_id
        assert body["title"] == "Hello"
        assert body["id"]

    def test_create_post_404_when_user_unknown(self, client: TestClient) -> None:
        response = client.post(
            "/posts",
            json={
                "user_id": "00000000-0000-0000-0000-000000000099",
                "title": "Hi",
                "content": "Body",
            },
        )

        assert response.status_code == 404

    def test_get_post(self, client: TestClient) -> None:
        user_id = self._register_user(client, email="getpost@example.com")
        created = client.post(
            "/posts",
            json={"user_id": user_id, "title": "T", "content": "C"},
        )
        post_id = created.json()["id"]

        response = client.get(f"/posts/{post_id}")

        assert response.status_code == 200
        assert response.json()["id"] == post_id

    def test_get_post_404(self, client: TestClient) -> None:
        response = client.get("/posts/00000000-0000-0000-0000-000000000002")

        assert response.status_code == 404

    def test_delete_post_returns_204(self, client: TestClient) -> None:
        user_id = self._register_user(client, email="delpost@example.com")
        created = client.post(
            "/posts",
            json={"user_id": user_id, "title": "D", "content": "D"},
        )
        post_id = created.json()["id"]

        response = client.delete(f"/posts/{post_id}")

        assert response.status_code == 204
        assert client.get(f"/posts/{post_id}").status_code == 404

    def test_delete_post_404(self, client: TestClient) -> None:
        response = client.delete("/posts/00000000-0000-0000-0000-000000000003")

        assert response.status_code == 404
