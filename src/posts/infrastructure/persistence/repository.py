from sqlalchemy import select
from sqlalchemy.orm import Session

from src.posts.application.ports.post_repository import IPostRepository
from src.posts.domain.post import Post
from src.posts.infrastructure.persistence.orm import PostORM


class SQLAlchemyPostRepository(IPostRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    async def add(self, post: Post) -> None:
        orm_post = PostORM(
            id=post.id,
            user_id=post.user_id,
            title=post.title,
            content=post.content,
            created_at=post.created_at,
        )
        self.db.add(orm_post)

    async def get_by_id(self, post_id: str) -> Post | None:
        orm_post = self.db.get(PostORM, post_id)
        if orm_post is None:
            return None
        return self._to_domain(orm_post)

    async def list_by_user_id(self, user_id: str) -> list[Post]:
        stmt = select(PostORM).where(PostORM.user_id == user_id)
        orm_posts = self.db.execute(stmt).scalars().all()
        return [self._to_domain(orm_post) for orm_post in orm_posts]

    async def delete(self, post_id: str) -> None:
        orm_post = self.db.get(PostORM, post_id)
        if orm_post is None:
            return
        self.db.delete(orm_post)

    @staticmethod
    def _to_domain(orm_post: PostORM) -> Post:
        return Post(
            id=orm_post.id,
            user_id=orm_post.user_id,
            title=orm_post.title,
            content=orm_post.content,
            created_at=orm_post.created_at,
        )
