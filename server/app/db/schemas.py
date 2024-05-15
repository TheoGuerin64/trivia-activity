from __future__ import annotations

from enum import Enum, auto

from sqlalchemy import CHAR, BigInteger, ForeignKey, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..api.trivia import Category, Difficulty
from . import Base


class User(Base):
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

    def __repr__(self) -> str:
        return f"<User id={self.id}>"


class RoomUser(Base):
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

    def __init__(self, room_id: int, user_id: int, socket_id: str) -> None:
        super().__init__(room_id=room_id, user_id=user_id, socket_id=socket_id)

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


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    channel_id: Mapped[int] = mapped_column(BigInteger, index=True, unique=True)
    state: Mapped[RoomState] = mapped_column(default=RoomState.LOBBY)
    leader_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    _room_users: Mapped[list[RoomUser]] = relationship(
        "RoomUser", back_populates="_room", cascade="delete"
    )
    _settings: Mapped[RoomSettings] = relationship(
        "RoomSettings", back_populates="_room", cascade="delete"
    )

    @property
    async def room_users(self) -> list[RoomUser]:
        return await self.awaitable_attrs._room_users

    @property
    async def settings(self) -> RoomSettings:
        return await self.awaitable_attrs._settings

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

    async def connected_room_users(self) -> tuple[RoomUser, ...]:
        return tuple(room_user for room_user in await self.room_users if room_user.connected)

    async def change_leader(self) -> None:
        self.leader_id = [
            room_user
            for room_user in await self.room_users
            if room_user.connected
            if room_user.user_id != self.leader_id
        ][0].user_id

    def __repr__(self) -> str:
        return f"<Room id={self.id}>"


class RoomSettings(Base):
    __tablename__ = "room_settings"

    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), primary_key=True)
    round_count: Mapped[int] = mapped_column(default=10)
    difficulty: Mapped[Difficulty] = mapped_column(default=Difficulty.RANDOM)
    category: Mapped[Category] = mapped_column(default=Category.RANDOM)

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
            "category": self.category.value,
        }

    def __repr__(self) -> str:
        return f"<RoomSettings room_id={self.room_id}>"
