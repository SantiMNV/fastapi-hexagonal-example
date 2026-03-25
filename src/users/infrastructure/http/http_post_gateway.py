from datetime import datetime

import httpx

from src.users.application.ports.post_gateway import IPostGateway
from src.users.domain.post_snapshot import PostSnapshot


class HttpPostGateway(IPostGateway):
    def __init__(
        self,
        base_url: str,
        *,
        internal_api_key: str | None = None,
        internal_api_header_name: str = "X-Internal-Token",
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._internal_api_key = internal_api_key
        self._internal_api_header_name = internal_api_header_name

    def _headers(self) -> dict[str, str]:
        if self._internal_api_key:
            return {self._internal_api_header_name: self._internal_api_key}
        return {}

    async def list_by_user_id(self, user_id: str) -> list[PostSnapshot]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._base_url}/internal/posts",
                params={"user_id": user_id},
                headers=self._headers(),
            )
        response.raise_for_status()
        return [self._to_snapshot(item) for item in response.json()]

    async def delete_by_user_id(self, user_id: str) -> None:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self._base_url}/internal/posts",
                params={"user_id": user_id},
                headers=self._headers(),
            )
        response.raise_for_status()

    @staticmethod
    def _to_snapshot(data: dict) -> PostSnapshot:
        return PostSnapshot(
            id=data["id"],
            user_id=data["user_id"],
            title=data["title"],
            content=data["content"],
            created_at=datetime.fromisoformat(data["created_at"]),
        )
