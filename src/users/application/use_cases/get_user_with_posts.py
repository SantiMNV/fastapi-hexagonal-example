from __future__ import annotations

from src.posts.application.ports.post_repository import PostRepository
from src.posts.domain.post import Post
from src.users.application.ports.user_repository import UserRepository
from src.users.domain.exceptions import UserNotFoundException
from src.users.domain.user import User


class GetUserWithPostsUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        post_repository: PostRepository,
    ) -> None:
        self._user_repository = user_repository
        self._post_repository = post_repository

    def execute(self, user_id: str) -> tuple[User, list[Post]]:
        user = self._user_repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundException(user_id)
        posts = self._post_repository.list_by_user_id(user_id)
        return (user, posts)
