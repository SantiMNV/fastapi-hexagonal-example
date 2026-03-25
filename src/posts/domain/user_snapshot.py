from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class UserSnapshot:
    id: str
    name: str
    email: str
    created_at: datetime
