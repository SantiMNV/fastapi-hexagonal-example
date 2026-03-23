from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from src.posts.application.ports.post_repository import PostRepository
from src.posts.domain.exceptions import PostAuthorNotFoundException
from src.posts.domain.post import Post
from src.shared.application.ports.unit_of_work import UnitOfWork
from src.users.application.ports.user_repository import UserRepository


class CreatePostUseCase:
    def __init__(
        self,
        post_repository: PostRepository,
        user_repository: UserRepository,
        uow: UnitOfWork,
    ) -> None:
        self._post_repository = post_repository
        self._user_repository = user_repository
        self._uow = uow

    def execute(self, user_id: str, title: str, content: str) -> Post:
        if self._user_repository.get_by_id(user_id) is None:
            raise PostAuthorNotFoundException(user_id)

        post = Post(
            id=str(uuid4()),
            user_id=user_id,
            title=title,
            content=content,
            created_at=datetime.now(UTC),
        )
        try:
            self._post_repository.add(post)
            self._uow.commit()
        except Exception:
            self._uow.rollback()
            raise
        return post
