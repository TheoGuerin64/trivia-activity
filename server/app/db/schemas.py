from __future__ import annotations

from enum import Enum, auto
from random import shuffle
from typing import Optional, Self

from sqlalchemy import CHAR, BigInteger, ForeignKey, Select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..api.trivia import Difficulty, Question
from . import BaseSchema


class User(BaseSchema):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    discord_id: Mapped[int] = mapped_column(BigInteger, index=True, unique=True)

    _room_users: Mapped[list[RoomUser]] = relationship(
        "RoomUser", back_populates="_user", cascade="delete"
    )

    @property
    async def room_users(self) -> list[RoomUser]:
        return await self.awaitable_attrs._room_users

    def __init__(self, discord_id: int) -> None:
        super().__init__(discord_id=discord_id)

    @staticmethod
    async def get(session: AsyncSession, id: int) -> User:
        """Raises `NoResultFound` if the result returns no rows."""
        return await session.get_one(User, id)

    @staticmethod
    async def get_by_discord_id(session: AsyncSession, discord_id: int) -> User:
        """
        Raises `NoResultFound` if the result returns no rows,
        or `MultipleResultsFound` if multiple rows would be returned.
        """
        statement = Select(User).where(User.discord_id == discord_id)
        result = await session.execute(statement)
        return result.scalar_one()

    @staticmethod
    async def get_or_create(session: AsyncSession, user_id: int) -> tuple[User, bool]:
        try:
            user = await User.get_by_discord_id(session, user_id)
        except NoResultFound:
            user = User(user_id)
            session.add(user)
            await session.flush()
            return user, True
        else:
            return user, False

    async def connect(self, session: AsyncSession, room: Room, sid: str) -> tuple[RoomUser, bool]:
        try:
            room_user = await RoomUser.get(session, self.id, room.id)
        except NoResultFound:
            room_user = RoomUser(self.id, room.id, sid)
            session.add(room_user)
            await session.flush()
            return room_user, True
        else:
            room_user.socket_id = sid
            room_user.connected = True
            await session.flush()
            return room_user, False

    def __repr__(self) -> str:
        return f"<User id={self.id}>"


class RoomUser(BaseSchema):
    __tablename__ = "room_users"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), primary_key=True)
    socket_id: Mapped[str] = mapped_column(CHAR(20), unique=True)
    connected: Mapped[bool] = mapped_column(default=True)

    _user: Mapped[User] = relationship("User", back_populates="_room_users")
    _room: Mapped[Room] = relationship("Room", back_populates="_room_users")

    @property
    async def user(self) -> User:
        return await self.awaitable_attrs._user

    @property
    async def room(self) -> Room:
        return await self.awaitable_attrs._room

    def __init__(self, user_id: int, room_id: int, socket_id: str) -> None:
        super().__init__(user_id=user_id, room_id=room_id, socket_id=socket_id)

    @staticmethod
    async def get(session: AsyncSession, user_id: int, room_id: int) -> RoomUser:
        """Raises `NoResultFound` if the result returns no rows."""
        return await session.get_one(RoomUser, (user_id, room_id))

    async def is_leader(self) -> bool:
        return (await self.room).leader_id == self.user_id

    def __repr__(self) -> str:
        return f"<RoomUser room_id={self.room_id} user_id={self.user_id}>"


class RoomState(Enum):
    LOBBY = auto()
    PLAYING = auto()


class Room(BaseSchema):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    channel_id: Mapped[int] = mapped_column(BigInteger, index=True, unique=True)
    state: Mapped[RoomState] = mapped_column(default=RoomState.LOBBY)
    leader_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    question_count: Mapped[int] = mapped_column(default=0)

    _room_users: Mapped[list[RoomUser]] = relationship(
        "RoomUser", back_populates="_room", cascade="delete"
    )
    _settings: Mapped[RoomSettings] = relationship(
        "RoomSettings", back_populates="_room", cascade="delete"
    )
    _question: Mapped[Optional[RoomQuestion]] = relationship(
        "RoomQuestion", back_populates="_room", cascade="delete"
    )

    @property
    async def room_users(self) -> list[RoomUser]:
        return await self.awaitable_attrs._room_users

    @property
    async def settings(self) -> RoomSettings:
        return await self.awaitable_attrs._settings

    @property
    async def question(self) -> Optional[RoomQuestion]:
        return await self.awaitable_attrs._question

    def __init__(self, channel_id: int, leader_id: int) -> None:
        super().__init__(channel_id=channel_id, leader_id=leader_id)

    @staticmethod
    async def get(session: AsyncSession, id: int) -> Room:
        """Raises `NoResultFound` if the result returns no rows."""
        return await session.get_one(Room, id)

    @staticmethod
    async def get_by_channel_id(session: AsyncSession, channel_id: int) -> Room:
        """
        Raises `NoResultFound` if the result returns no rows,
        or `MultipleResultsFound` if multiple rows would be returned.
        """
        statement = Select(Room).where(Room.channel_id == channel_id)
        result = await session.execute(statement)
        return result.scalar_one()

    @staticmethod
    async def get_or_create(
        session: AsyncSession, user_id: int, channel_id: int
    ) -> tuple[Room, bool]:
        """Raises `MultipleResultsFound` if multiple rows would be returned."""
        try:
            room = await Room.get_by_channel_id(session, channel_id)
        except NoResultFound:
            room = Room(channel_id, user_id)
            session.add(room)
            await session.flush()
            return room, True
        else:
            return room, False

    async def connected_room_users(self) -> tuple[RoomUser, ...]:
        return tuple(room_user for room_user in await self.room_users if room_user.connected)

    async def change_leader(self) -> RoomUser:
        leader = [
            room_user
            for room_user in await self.room_users
            if room_user.connected
            if room_user.user_id != self.leader_id
        ][0]
        self.leader_id = leader.user_id
        return leader

    def __repr__(self) -> str:
        return f"<Room id={self.id}>"


class RoomSettings(BaseSchema):
    __tablename__ = "room_settings"

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), primary_key=True)
    round_count: Mapped[int] = mapped_column(default=10)
    difficulty: Mapped[Difficulty] = mapped_column(default=Difficulty.RANDOM)
    category: Mapped[int] = mapped_column(default=0)

    _room: Mapped[Room] = relationship("Room", back_populates="_settings")

    @property
    async def room(self) -> Room:
        return await self.awaitable_attrs._room

    def __init__(self, room_id: int) -> None:
        super().__init__(room_id=room_id)

    @staticmethod
    async def get(session: AsyncSession, room_id: int) -> RoomSettings:
        """Raises `NoResultFound` if the result returns no rows."""
        return await session.get_one(RoomSettings, room_id)

    def data(self) -> dict[str, str | int]:
        return {
            "round_count": self.round_count,
            "difficulty": self.difficulty.value,
            "category": self.category,
        }

    def __repr__(self) -> str:
        return f"<RoomSettings room_id={self.room_id}>"


class RoomQuestion(BaseSchema):
    __tablename__ = "questions"

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), primary_key=True)
    category: Mapped[str]
    difficulty: Mapped[Difficulty]
    question: Mapped[str]
    correct_answer: Mapped[str]
    incorrect_answer_1: Mapped[str]
    incorrect_answer_2: Mapped[Optional[str]] = mapped_column(default=None)
    incorrect_answer_3: Mapped[Optional[str]] = mapped_column(default=None)

    _room: Mapped[Optional[Room]] = relationship("Room", back_populates="_question")

    @property
    async def room(self) -> Optional[Room]:
        return await self.awaitable_attrs._room

    def __init__(
        self,
        room_id: int,
        category: str,
        difficulty: Difficulty,
        question: str,
        correct_answer: str,
        incorrect_answer_1: str,
        incorrect_answer_2: Optional[str],
        incorrect_answer_3: Optional[str],
    ) -> None:
        super().__init__(
            room_id=room_id,
            category=category,
            difficulty=difficulty,
            question=question,
            correct_answer=correct_answer,
            incorrect_answer_1=incorrect_answer_1,
            incorrect_answer_2=incorrect_answer_2,
            incorrect_answer_3=incorrect_answer_3,
        )

    @classmethod
    def from_model(cls, room_id: int, question: Question) -> Self:
        return cls(
            room_id=room_id,
            category=question.category,
            difficulty=Difficulty(question.difficulty),
            question=question.question,
            correct_answer=question.correct_answer,
            incorrect_answer_1=question.incorrect_answers[0],
            incorrect_answer_2=(
                question.incorrect_answers[1] if len(question.incorrect_answers) > 1 else None
            ),
            incorrect_answer_3=(
                question.incorrect_answers[2] if len(question.incorrect_answers) > 2 else None
            ),
        )

    def to_client(self) -> dict[str, str | list[str]]:
        answers = [self.correct_answer, self.incorrect_answer_1]
        if self.incorrect_answer_2:
            answers.append(self.incorrect_answer_2)
        if self.incorrect_answer_3:
            answers.append(self.incorrect_answer_3)
        shuffle(answers)

        return {
            "category": self.category,
            "difficulty": self.difficulty.value,
            "question": self.question,
            "answers": answers,
        }

    def __repr__(self) -> str:
        return f"<Question id={self.room_id}>"
