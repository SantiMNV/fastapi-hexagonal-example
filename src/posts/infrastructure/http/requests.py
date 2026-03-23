from pydantic import BaseModel


class CreatePostRequest(BaseModel):
    user_id: str
    title: str
    content: str
