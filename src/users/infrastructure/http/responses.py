from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from src.shared.infrastructure.http.responses import PostResponse


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserWithPostsResponse(BaseModel):
    user: UserResponse
    posts: list[PostResponse]
