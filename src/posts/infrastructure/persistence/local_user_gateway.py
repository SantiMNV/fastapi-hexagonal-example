from src.posts.application.ports.user_gateway import IUserGateway
from src.posts.domain.user_snapshot import UserSnapshot
from src.users.application.use_cases.get_user import GetUserUseCase
from src.users.domain.exceptions import UserNotFoundException


class LocalUserGateway(IUserGateway):
    """Resolves users via GetUserUseCase using the shared DB session (monolith / tests)."""

    def __init__(self, get_user: GetUserUseCase) -> None:
        self._get_user = get_user

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
