from src.posts.domain.eligibility import PostAuthorEligibilityReason
from src.shared.domain.base_exception import BaseAppException


class PostNotFoundException(BaseAppException):
    def __init__(self, post_id: str) -> None:
        super().__init__(f"Post '{post_id}' not found", code="post_not_found")


class PostAuthorNotEligibleException(BaseAppException):
    def __init__(self, user_id: str, *, reason: PostAuthorEligibilityReason | None = None) -> None:
        super().__init__(
            f"User '{user_id}' is not allowed to create posts",
            code="post_author_not_eligible",
        )
        self.eligibility_reason = reason
