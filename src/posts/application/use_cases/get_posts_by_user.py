from __future__ import annotations

from src.posts.application.ports.post_repository import IPostRepository
from src.posts.domain.post import Post


class GetPostsByUserUseCase:
    def __init__(self, post_repository: IPostRepository) -> None:
        self._post_repository = post_repository

    async def execute(self, user_id: str) -> list[Post]:
        return await self._post_repository.list_by_user_id(user_id)
