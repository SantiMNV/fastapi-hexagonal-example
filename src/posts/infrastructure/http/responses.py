from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PostResponse(BaseModel):
    id: str
    user_id: str
    title: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
