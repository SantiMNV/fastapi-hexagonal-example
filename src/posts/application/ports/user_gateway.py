from typing import Protocol

from src.posts.domain.user_snapshot import UserSnapshot


class IUserGateway(Protocol):
    async def get_by_id(self, user_id: str) -> UserSnapshot | None: ...
