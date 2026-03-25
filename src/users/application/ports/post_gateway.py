from typing import Protocol

from src.users.domain.post_snapshot import PostSnapshot


class IPostGateway(Protocol):
    async def list_by_user_id(self, user_id: str) -> list[PostSnapshot]: ...

    async def delete_by_user_id(self, user_id: str) -> None: ...
