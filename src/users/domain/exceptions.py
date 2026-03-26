from src.shared.domain.base_exception import BaseAppException


class UserNotFoundException(BaseAppException):
    def __init__(self, user_id: str) -> None:
        super().__init__(f"User '{user_id}' not found", code="user_not_found")


class UserAlreadyExistsException(BaseAppException):
    def __init__(self, email: str) -> None:
        super().__init__(f"User with email '{email}' already exists", code="user_already_exists")


class UserCannotCreatePostsYetException(BaseAppException):
    def __init__(self, user_id: str) -> None:
        super().__init__(
            f"User '{user_id}' cannot create posts yet (account too new)",
            code="user_cannot_create_posts_yet",
        )
