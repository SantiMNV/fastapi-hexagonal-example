from dataclasses import dataclass
from enum import Enum


class PostAuthorEligibilityReason(str, Enum):
    TOO_EARLY = "too_early"
    SUSPENDED = "suspended"
    NOT_VERIFIED = "not_verified"
    NOT_FOUND = "not_found"


@dataclass
class PostAuthorEligibility:
    allowed: bool
    reason: PostAuthorEligibilityReason | None = None
