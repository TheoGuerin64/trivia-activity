from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class Auth(BaseModel):
    code: str = Field(max_length=30)
    channel_id: PositiveInt = Field(lt=2**64)


class Settings(BaseModel):
    round_count: Optional[int] = Field(ge=1, le=10, default=None)
    difficulty: Optional[int] = Field(ge=0, le=3, default=None)
