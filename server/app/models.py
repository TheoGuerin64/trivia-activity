from pydantic import BaseModel, Field, PositiveInt

from .api.trivia import Difficulty


class Auth(BaseModel):
    code: str = Field(max_length=30)
    channel_id: PositiveInt = Field(le=2**64 - 1)


class Settings(BaseModel):
    round_count: int = Field(ge=1, le=10)
    difficulty: Difficulty
    category: PositiveInt
