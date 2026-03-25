from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class PostSnapshot:
    id: str
    user_id: str
    title: str
    content: str
    created_at: datetime
