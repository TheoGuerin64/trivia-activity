from pydantic import BaseModel, Field


class Auth(BaseModel):
    code: str = Field(max_length=30)
    channel_id: str = Field(pattern=r"\d{1,20}")
