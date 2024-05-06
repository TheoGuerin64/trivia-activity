from pydantic import BaseModel, Field


class Auth(BaseModel):
    code: str = Field(max_length=30)
    channel_id: str = Field(max_length=20)
