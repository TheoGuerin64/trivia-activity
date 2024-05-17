from pydantic import BaseModel, Field, PositiveInt

from .api.trivia import Difficulty


class Auth(BaseModel):
    code: str = Field(max_length=30)
    channel_id: PositiveInt = Field(lt=2**64)


class Settings(BaseModel):
    round_count: int | None = Field(ge=1, le=10, default=None)
    difficulty: Difficulty | None = Field(default=None)
    category: int | None = Field(default=None)

    def data(self) -> dict[str, int | str]:
        result = {}
        if self.round_count is not None:
            result["round_count"] = self.round_count
        if self.difficulty is not None:
            result["difficulty"] = self.difficulty.name
        if self.category is not None:
            result["category"] = self.category
        return result
