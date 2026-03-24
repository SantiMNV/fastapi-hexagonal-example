from __future__ import annotations

import httpx

from src.posts.application.ports.post_repository import IPostRepository
from src.posts.domain.exceptions import PostAuthorNotFoundException
from src.posts.domain.post import Post
from src.posts.infrastructure.http.responses import PostResponse


def _post_from_payload(data: object) -> Post:
    body = PostResponse.model_validate(data)
    return Post(
        id=body.id,
        user_id=body.user_id,
        title=body.title,
        content=body.content,
        created_at=body.created_at,
    )


class PostRepositoryGateway(IPostRepository):
    def __init__(self, *, client: httpx.AsyncClient, base_url: str) -> None:
        self._client = client
        self._base = base_url.rstrip("/")

    async def add(self, post: Post) -> None:
        response = await self._client.post(
            f"{self._base}/posts",
            json={
                "user_id": post.user_id,
                "title": post.title,
                "content": post.content,
                "id": post.id,
                "created_at": post.created_at.isoformat(),
            },
        )
        if response.status_code == 404:
            raise PostAuthorNotFoundException(post.user_id)
        response.raise_for_status()

    async def get_by_id(self, post_id: str) -> Post | None:
        response = await self._client.get(f"{self._base}/posts/{post_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return _post_from_payload(response.json())

    async def list_by_user_id(self, user_id: str) -> list[Post]:
        response = await self._client.get(f"{self._base}/posts/by-user/{user_id}")
        response.raise_for_status()
        return [_post_from_payload(item) for item in response.json()]

    async def delete(self, post_id: str) -> None:
        response = await self._client.delete(f"{self._base}/posts/{post_id}")
        if response.status_code == 404:
            return
        response.raise_for_status()
