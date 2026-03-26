from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from src.posts.application.ports.post_repository import IPostRepository
from src.posts.application.ports.user_gateway import IUserGateway
from src.posts.domain.exceptions import PostAuthorNotEligibleException
from src.posts.domain.post import Post
from src.shared.application.ports.unit_of_work import UnitOfWork


class CreatePostUseCase:
    def __init__(
        self,
        post_repository: IPostRepository,
        user_gateway: IUserGateway,
        uow: UnitOfWork,
    ) -> None:
        self._post_repository = post_repository
        self._user_gateway = user_gateway
        self._uow = uow

    async def execute(self, user_id: str, title: str, content: str) -> Post:
        eligibility = await self._user_gateway.get_post_author_eligibility(user_id)
        if not eligibility.allowed:
            raise PostAuthorNotEligibleException(user_id, reason=eligibility.reason)

        post = Post(
            id=str(uuid4()),
            user_id=user_id,
            title=title,
            content=content,
            created_at=datetime.now(UTC),
        )
        try:
            await self._post_repository.add(post)
            self._uow.commit()
        except Exception:
            self._uow.rollback()
            raise
        return post
