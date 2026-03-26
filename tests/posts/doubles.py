from datetime import UTC, datetime, timedelta
from uuid import uuid4

from src.posts.application.ports.user_gateway import IUserGateway
from src.posts.domain.eligibility import PostAuthorEligibility, PostAuthorEligibilityReason
from src.posts.domain.post import Post
from src.posts.domain.user_snapshot import UserSnapshot
from tests.users.doubles import (
    InMemoryPostGateway,
    InMemoryPostRepository,
    InMemoryUserRepository,
    NoOpUnitOfWork,
    sample_user,
)


class InMemoryUserGateway(IUserGateway):
    def __init__(self, *, min_account_age: timedelta = timedelta(0)) -> None:
        self.snapshots: dict[str, UserSnapshot] = {}
        self._min_account_age = min_account_age

    async def get_post_author_eligibility(self, user_id: str) -> PostAuthorEligibility:
        snap = self.snapshots.get(user_id)
        if snap is None:
            return PostAuthorEligibility(allowed=False, reason=PostAuthorEligibilityReason.NOT_FOUND)
        if self._min_account_age.total_seconds() > 0:
            created = snap.created_at
            if created.tzinfo is None:
                created = created.replace(tzinfo=UTC)
            if datetime.now(UTC) - created < self._min_account_age:
                return PostAuthorEligibility(allowed=False, reason=PostAuthorEligibilityReason.TOO_EARLY)
        return PostAuthorEligibility(allowed=True)

    async def get_by_id(self, user_id: str) -> UserSnapshot | None:
        return self.snapshots.get(user_id)


__all__ = [
    "InMemoryPostGateway",
    "InMemoryPostRepository",
    "InMemoryUserGateway",
    "InMemoryUserRepository",
    "NoOpUnitOfWork",
    "sample_post",
    "sample_user",
]


def sample_post(
    *,
    post_id: str | None = None,
    user_id: str,
    title: str = "Title",
    content: str = "Content",
) -> Post:
    return Post(
        id=post_id or str(uuid4()),
        user_id=user_id,
        title=title,
        content=content,
        created_at=datetime.now(UTC),
    )
