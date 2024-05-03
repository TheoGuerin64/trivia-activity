from pydantic import BaseModel, Field


class Auth(BaseModel):
    code: str
    channel_id: str = Field(pattern=r"\d{1,20}")
