from pydantic import BaseModel, Field, PositiveInt

from .db.schemas import Difficulty


class Auth(BaseModel):
    code: str = Field(max_length=30)
    channel_id: PositiveInt = Field(lt=2**64)


class Settings(BaseModel):
    round_count: int | None = Field(ge=1, le=10, default=None)
    difficulty: Difficulty | None = Field(default=None)
