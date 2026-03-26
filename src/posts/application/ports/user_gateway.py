from typing import Protocol

from src.posts.domain.eligibility import PostAuthorEligibility
from src.posts.domain.user_snapshot import UserSnapshot


class IUserGateway(Protocol):
    async def get_by_id(self, user_id: str) -> UserSnapshot | None: ...

    async def get_post_author_eligibility(self, user_id: str) -> PostAuthorEligibility: ...
