from __future__ import annotations

from src.posts.application.ports.post_repository import IPostRepository
from src.posts.domain.exceptions import PostNotFoundException
from src.posts.domain.post import Post


class GetPostUseCase:
    def __init__(self, repository: IPostRepository) -> None:
        self._repository = repository

    async def execute(self, post_id: str) -> Post:
        post = await self._repository.get_by_id(post_id)
        if post is None:
            raise PostNotFoundException(post_id)
        return post
