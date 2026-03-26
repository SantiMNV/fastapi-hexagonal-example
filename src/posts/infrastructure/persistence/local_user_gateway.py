from src.posts.application.ports.user_gateway import IUserGateway
from src.posts.domain.eligibility import PostAuthorEligibility, PostAuthorEligibilityReason
from src.posts.domain.user_snapshot import UserSnapshot
from src.users.application.use_cases.get_user import GetUserUseCase
from src.users.application.use_cases.verify_user_can_create_post import (
    VerifyUserCanCreatePostUseCase,
)
from src.users.domain.exceptions import UserCannotCreatePostsYetException, UserNotFoundException


class LocalUserGateway(IUserGateway):
    """Resolves users via user use cases using the shared DB session (monolith / tests)."""

    def __init__(
        self,
        get_user: GetUserUseCase,
        verify_can_create_post: VerifyUserCanCreatePostUseCase,
    ) -> None:
        self._get_user = get_user
        self._verify_can_create_post = verify_can_create_post

    async def get_post_author_eligibility(self, user_id: str) -> PostAuthorEligibility:
        try:
            await self._verify_can_create_post.execute(user_id)
            return PostAuthorEligibility(allowed=True)
        except UserNotFoundException:
            return PostAuthorEligibility(allowed=False, reason=PostAuthorEligibilityReason.NOT_FOUND)
        except UserCannotCreatePostsYetException:
            return PostAuthorEligibility(allowed=False, reason=PostAuthorEligibilityReason.TOO_EARLY)

    async def get_by_id(self, user_id: str) -> UserSnapshot | None:
        try:
            user = await self._get_user.execute(user_id)
        except UserNotFoundException:
            return None
        return UserSnapshot(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
        )
