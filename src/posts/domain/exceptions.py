from src.shared.domain.base_exception import BaseAppException


class PostNotFoundException(BaseAppException):
    def __init__(self, post_id: str) -> None:
        super().__init__(f"Post '{post_id}' not found", code="post_not_found")


class PostAuthorNotFoundException(BaseAppException):
    def __init__(self, user_id: str) -> None:
        super().__init__(f"User '{user_id}' not found", code="post_author_not_found")
