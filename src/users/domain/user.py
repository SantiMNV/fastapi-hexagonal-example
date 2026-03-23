from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class User:
    id: str
    name: str
    email: str
    created_at: datetime
