from __future__ import annotations

from src.posts.application.ports.post_repository import PostRepository
from src.posts.domain.exceptions import PostAuthorNotFoundException
from src.posts.domain.post import Post
from src.users.application.ports.user_repository import UserRepository


class ListUserPostsUseCase:
    def __init__(
        self,
        post_repository: PostRepository,
        user_repository: UserRepository,
    ) -> None:
        self._post_repository = post_repository
        self._user_repository = user_repository

    def execute(self, user_id: str) -> list[Post]:
        if self._user_repository.get_by_id(user_id) is None:
            raise PostAuthorNotFoundException(user_id)
        return self._post_repository.list_by_user_id(user_id)
