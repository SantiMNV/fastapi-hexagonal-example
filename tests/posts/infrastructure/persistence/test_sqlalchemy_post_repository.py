from sqlalchemy.orm import Session

from src.posts.infrastructure.persistence.repository import SQLAlchemyPostRepository
from src.users.infrastructure.persistence.repository import SQLAlchemyUserRepository
from tests.posts.doubles import sample_post
from tests.users.doubles import sample_user


class TestSQLAlchemyPostRepository:
    async def test_add_get_and_list(self, db_session: Session) -> None:
        users = SQLAlchemyUserRepository(db_session)
        posts = SQLAlchemyPostRepository(db_session)
        user = sample_user(email="postowner@example.com")
        await users.add(user)
        db_session.flush()
        post = sample_post(user_id=user.id, title="One", content="A")
        await posts.add(post)
        db_session.flush()

        loaded = await posts.get_by_id(post.id)
        assert loaded is not None
        assert loaded.id == post.id
        assert loaded.user_id == post.user_id
        assert loaded.title == post.title
        assert loaded.content == post.content

        listed = await posts.list_by_user_id(user.id)
        assert len(listed) == 1
        assert listed[0].id == post.id

    async def test_get_by_id_returns_none_when_missing(self, db_session: Session) -> None:
        posts = SQLAlchemyPostRepository(db_session)

        assert await posts.get_by_id("missing") is None

    async def test_delete_removes_row(self, db_session: Session) -> None:
        users = SQLAlchemyUserRepository(db_session)
        posts = SQLAlchemyPostRepository(db_session)
        user = sample_user()
        await users.add(user)
        db_session.flush()
        post = sample_post(user_id=user.id)
        await posts.add(post)
        db_session.flush()

        await posts.delete(post.id)
        db_session.flush()

        assert await posts.get_by_id(post.id) is None

    async def test_delete_is_noop_when_row_missing(self, db_session: Session) -> None:
        posts = SQLAlchemyPostRepository(db_session)

        await posts.delete("nope")

        assert await posts.get_by_id("nope") is None
