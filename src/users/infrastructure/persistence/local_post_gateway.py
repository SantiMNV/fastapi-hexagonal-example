from src.posts.application.use_cases import DeleteUserPostsUseCase, GetPostsByUserUseCase
from src.users.application.ports.post_gateway import IPostGateway
from src.users.domain.post_snapshot import PostSnapshot


class LocalPostGateway(IPostGateway):
    """Reads and deletes posts via use cases using the shared DB session (monolith / tests)."""

    def __init__(self, list_uc: GetPostsByUserUseCase, delete_uc: DeleteUserPostsUseCase) -> None:
        self._list_uc = list_uc
        self._delete_uc = delete_uc

    async def list_by_user_id(self, user_id: str) -> list[PostSnapshot]:
        posts = await self._list_uc.execute(user_id)
        return [
            PostSnapshot(
                id=p.id,
                user_id=p.user_id,
                title=p.title,
                content=p.content,
                created_at=p.created_at,
            )
            for p in posts
        ]

    async def delete_by_user_id(self, user_id: str) -> None:
        await self._delete_uc.execute(user_id)
