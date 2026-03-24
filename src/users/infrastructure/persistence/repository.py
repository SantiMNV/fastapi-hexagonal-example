from sqlalchemy import select
from sqlalchemy.orm import Session

from src.users.application.ports.user_repository import IUserRepository
from src.users.domain.user import User
from src.users.infrastructure.persistence.orm import UserORM


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    async def add(self, user: User) -> None:
        orm_user = UserORM(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
        )
        self.db.add(orm_user)

    async def get_by_id(self, user_id: str) -> User | None:
        orm_user = self.db.get(UserORM, user_id)
        if orm_user is None:
            return None
        return self._to_domain(orm_user)

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(UserORM).where(UserORM.email == email)
        orm_user = self.db.execute(stmt).scalar_one_or_none()
        if orm_user is None:
            return None
        return self._to_domain(orm_user)

    async def delete(self, user_id: str) -> None:
        orm_user = self.db.get(UserORM, user_id)
        if orm_user is None:
            return
        self.db.delete(orm_user)

    @staticmethod
    def _to_domain(orm_user: UserORM) -> User:
        return User(
            id=orm_user.id,
            name=orm_user.name,
            email=orm_user.email,
            created_at=orm_user.created_at,
        )
