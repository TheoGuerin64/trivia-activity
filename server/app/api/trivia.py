from enum import Enum, StrEnum, auto
from html import unescape

import aiohttp
from pydantic import BaseModel, field_validator

from .exceptions import APIError


class ErrorCode(Enum):
    SUCCESS = 0
    NO_RESULTS = 1
    INVALID_PARAMETER = 2
    TOKEN_NOT_FOUND = 3
    TOKEN_EMPTY = 4
    RATE_LIMIT = 5


class Difficulty(StrEnum):
    RANDOM = auto()
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()


class Question(BaseModel):
    type: str
    category: str
    difficulty: str
    question: str
    correct_answer: str
    incorrect_answers: list[str]

    @field_validator("category", "question", "correct_answer", "incorrect_answers")
    def unescape_html(cls, value):
        if isinstance(value, list):
            return [unescape(item) for item in value]
        return unescape(value)


async def question(category: int, difficulty: Difficulty) -> Question:
    params: dict[str, str | list[str]] = {"amount": "1"}
    if category != 0:
        params["category"] = str(category)
    if difficulty != Difficulty.RANDOM:
        params["difficulty"] = str(difficulty.value)

    async with aiohttp.ClientSession() as session:
        async with session.get("https://opentdb.com/api.php", params=params) as response:
            match response.status:
                case 200:
                    pass
                case 429:
                    raise APIError("Rate limit exceeded")
                case _:
                    raise APIError("Request failed")

            json = await response.json()

            error_code = ErrorCode(json["response_code"])
            if error_code != ErrorCode.SUCCESS:
                raise APIError(f"API error: {error_code.name}")

            return Question.model_validate(json["results"][0])
