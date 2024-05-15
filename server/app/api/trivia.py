from enum import Enum, StrEnum, auto
from html import unescape
from random import shuffle

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


class Category(Enum):
    RANDOM = 0
    GENERAL_KNOWLEDGE = 9
    ENTERTAINMENT_BOOKS = 10
    ENTERTAINMENT_FILM = 11
    ENTERTAINMENT_MUSIC = 12
    ENTERTAINMENT_MUSICALS_THEATRES = 13
    ENTERTAINMENT_TELEVISION = 14
    ENTERTAINMENT_VIDEO_GAMES = 15
    ENTERTAINMENT_BOARD_GAMES = 16
    SCIENCE_NATURE = 17
    SCIENCE_COMPUTERS = 18
    SCIENCE_MATHEMATICS = 19
    MYTHOLOGY = 20
    SPORTS = 21
    GEOGRAPHY = 22
    HISTORY = 23
    POLITICS = 24
    ART = 25
    CELEBRITIES = 26
    ANIMALS = 27
    VEHICLES = 28
    ENTERTAINMENT_COMICS = 29
    SCIENCE_GADGETS = 30
    ENTERTAINMENT_JAPANESE_ANIME_MANGA = 31
    ENTERTAINMENT_CARTOON_ANIMATIONS = 32


class Difficulty(StrEnum):
    RANDOM = auto()
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()


class Question(BaseModel):
    type: str
    difficulty: str
    category: str
    question: str
    correct_answer: str
    incorrect_answers: list[str]

    @field_validator("question", "correct_answer", "incorrect_answers")
    def unescape_html(cls, value):
        return unescape(value)

    def data(self) -> dict[str, str | list[str]]:
        answers = [self.correct_answer, *self.incorrect_answers]
        shuffle(answers)
        return {
            "difficulty": self.difficulty,
            "category": self.category,
            "question": self.question,
            "answers": answers,
        }


async def question(category: Category, difficulty: Difficulty) -> Question:
    params: dict[str, str | list[str]] = {"amount": "1"}
    if category != Category.RANDOM:
        params["category"] = str(category.value)
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
