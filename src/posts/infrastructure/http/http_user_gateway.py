from datetime import datetime

import httpx

from src.posts.application.ports.user_gateway import IUserGateway
from src.posts.domain.eligibility import PostAuthorEligibility, PostAuthorEligibilityReason
from src.posts.domain.user_snapshot import UserSnapshot


class HttpUserGateway(IUserGateway):
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

    async def get_post_author_eligibility(self, user_id: str) -> PostAuthorEligibility:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._base_url}/internal/users/{user_id}/posting-eligibility",
                headers=self._headers(),
            )
        if response.status_code == 404:
            return PostAuthorEligibility(allowed=False, reason=PostAuthorEligibilityReason.NOT_FOUND)
        if response.status_code == 403:
            return PostAuthorEligibility(allowed=False, reason=PostAuthorEligibilityReason.TOO_EARLY)
        response.raise_for_status()
        return PostAuthorEligibility(allowed=True)

    async def get_by_id(self, user_id: str) -> UserSnapshot | None:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._base_url}/internal/users/{user_id}",
                headers=self._headers(),
            )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        data = response.json()
        return UserSnapshot(
            id=data["id"],
            name=data["name"],
            email=str(data["email"]),
            created_at=datetime.fromisoformat(data["created_at"]),
        )
