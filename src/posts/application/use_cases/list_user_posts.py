from __future__ import annotations

from src.posts.application.ports.post_repository import IPostRepository
from src.posts.domain.exceptions import PostAuthorNotFoundException
from src.posts.domain.post import Post
from src.users.application.ports.user_repository import IUserRepository


class ListUserPostsUseCase:
    def __init__(
        self,
        post_repository: IPostRepository,
        user_repository: IUserRepository,
    ) -> None:
        self._post_repository = post_repository
        self._user_repository = user_repository

    async def execute(self, user_id: str) -> list[Post]:
        if await self._user_repository.get_by_id(user_id) is None:
            raise PostAuthorNotFoundException(user_id)
        return await self._post_repository.list_by_user_id(user_id)
