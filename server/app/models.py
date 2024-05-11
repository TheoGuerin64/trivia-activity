from pydantic import BaseModel, Field, PositiveInt


class Auth(BaseModel):
    code: str = Field(max_length=30)
    channel_id: PositiveInt
