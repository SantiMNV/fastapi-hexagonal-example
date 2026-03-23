from __future__ import annotations

import httpx

from src.posts.infrastructure.http.responses import PostResponse


def list_posts_for_user(*, posts_bridge: httpx.Client, user_id: str) -> list[PostResponse]:
    """httpx.Client in prod, or TestClient when POSTS_SERVICE_BASE_URL is __embedded_posts__."""
    response = posts_bridge.get(f"/posts/by-user/{user_id}")
    response.raise_for_status()
    raw = response.json()
    return [PostResponse.model_validate(item) for item in raw]
