from dataclasses import dataclass
from datetime import UTC, datetime, timedelta


@dataclass(slots=True)
class User:
    id: str
    name: str
    email: str
    created_at: datetime

    def can_create_posts(
        self,
        *,
        now: datetime,
        min_account_age: timedelta,
    ) -> bool:
        """Product rule: new accounts wait out spam / onboarding window before posting."""
        if min_account_age.total_seconds() <= 0:
            return True
        created = self.created_at
        if created.tzinfo is None:
            created = created.replace(tzinfo=UTC)
        return (now - created) >= min_account_age
