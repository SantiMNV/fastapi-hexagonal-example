from src.posts.infrastructure.persistence.orm import PostORM


class TestPostORM:
    def test_maps_posts_table(self) -> None:
        assert PostORM.__tablename__ == "posts"
