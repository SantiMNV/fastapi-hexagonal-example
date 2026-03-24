import asyncio
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime

import httpx

from src.posts.domain.post import Post
from src.posts.infrastructure.http.post_repository_gateway import PostRepositoryGateway


def _run_gateway_test(
    client: httpx.AsyncClient,
    test_fn: Callable[[], Awaitable[None]],
) -> None:
    async def runner() -> None:
        try:
            await test_fn()
        finally:
            await client.aclose()

    asyncio.run(runner())


class TestPostRepositoryGateway:
    def test_get_by_id_returns_none_on_404(self) -> None:
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(404)

        transport = httpx.MockTransport(handler)
        client = httpx.AsyncClient(transport=transport, base_url="http://svc")
        gw = PostRepositoryGateway(client=client, base_url="http://svc")

        async def body() -> None:
            assert await gw.get_by_id("missing") is None

        _run_gateway_test(client, body)

    def test_get_by_id_returns_post(self) -> None:
        created = datetime(2024, 1, 2, tzinfo=UTC)
        payload = {
            "id": "p1",
            "user_id": "u1",
            "title": "Hi",
            "content": "Body",
            "created_at": created.isoformat(),
        }

        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/posts/p1"
            return httpx.Response(200, json=payload)

        transport = httpx.MockTransport(handler)
        client = httpx.AsyncClient(transport=transport, base_url="http://svc")
        gw = PostRepositoryGateway(client=client, base_url="http://svc")

        async def body() -> None:
            post = await gw.get_by_id("p1")
            assert post == Post(
                id="p1",
                user_id="u1",
                title="Hi",
                content="Body",
                created_at=created,
            )

        _run_gateway_test(client, body)

    def test_list_by_user_id(self) -> None:
        created = datetime(2024, 1, 2, tzinfo=UTC)
        row = {
            "id": "p1",
            "user_id": "u1",
            "title": "Hi",
            "content": "Body",
            "created_at": created.isoformat(),
        }

        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/posts/by-user/u1"
            return httpx.Response(200, json=[row])

        transport = httpx.MockTransport(handler)
        client = httpx.AsyncClient(transport=transport, base_url="http://svc")
        gw = PostRepositoryGateway(client=client, base_url="http://svc")

        async def body() -> None:
            posts = await gw.list_by_user_id("u1")
            assert len(posts) == 1
            assert posts[0].id == "p1"

        _run_gateway_test(client, body)
