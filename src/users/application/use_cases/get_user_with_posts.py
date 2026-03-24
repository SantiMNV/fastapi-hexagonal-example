from __future__ import annotations

from src.posts.application.ports.post_repository import IPostRepository
from src.posts.domain.post import Post
from src.users.application.ports.user_repository import IUserRepository
from src.users.domain.exceptions import UserNotFoundException
from src.users.domain.user import User


class GetUserWithPostsUseCase:
    def __init__(
        self,
        user_repository: IUserRepository,
        post_repository: IPostRepository,
    ) -> None:
        self._user_repository = user_repository
        self._post_repository = post_repository

    async def execute(self, user_id: str) -> tuple[User, list[Post]]:
        user = await self._user_repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundException(user_id)
        posts = await self._post_repository.list_by_user_id(user_id)
        return (user, posts)
