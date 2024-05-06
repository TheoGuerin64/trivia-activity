from typing import List, Optional

from sqlalchemy import CHAR, ForeignKey, Select, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    discord_id: Mapped[str] = mapped_column(String(20), index=True, unique=True)
    socket_id: Mapped[str] = mapped_column(CHAR(20), unique=True)
    room_id: Mapped[Optional[int]] = mapped_column(ForeignKey("rooms.id"), index=True)
    connected: Mapped[bool] = mapped_column(default=True)

    room: Mapped["Room"] = relationship("Room", back_populates="users")

    def __init__(self, session: AsyncSession, discord_id: str, socket_id: str) -> None:
        super().__init__(
            discord_id=discord_id,
            socket_id=socket_id,
        )
        session.add(self)

    @staticmethod
    async def get(session: AsyncSession, id: int) -> "User":
        """
        Raises `NoResultFound` if the result returns no rows,
        or `MultipleResultsFound` if multiple rows would be returned.
        """
        return await session.get_one(User, id)

    @staticmethod
    async def get_by_discord_id(session: AsyncSession, discord_id: str) -> "User":
        """
        Raises `NoResultFound` if the result returns no rows,
        or `MultipleResultsFound` if multiple rows would be returned.
        """
        statement = Select(User).where(User.discord_id == discord_id)
        result = await session.execute(statement)
        return result.scalar_one()

    def __repr__(self) -> str:
        return f"<User id={self.id} connected={self.connected}>"


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    channel_id: Mapped[str] = mapped_column(String(20), index=True, unique=True)

    users: Mapped[List["User"]] = relationship("User", back_populates="room")

    def __init__(self, session: AsyncSession, channel_id: str) -> None:
        super().__init__(
            channel_id=channel_id,
        )
        session.add(self)

    @staticmethod
    async def get(session: AsyncSession, id: int) -> "Room":
        """
        Raises `NoResultFound` if the result returns no rows,
        or `MultipleResultsFound` if multiple rows would be returned.
        """
        return await session.get_one(Room, id)

    @staticmethod
    async def get_by_channel_id(session: AsyncSession, channel_id: str) -> "Room":
        """
        Raises `NoResultFound` if the result returns no rows,
        or `MultipleResultsFound` if multiple rows would be returned.
        """
        statement = Select(Room).where(Room.channel_id == channel_id)
        result = await session.execute(statement)
        return result.scalar_one()

    def __repr__(self) -> str:
        return f"<Room id={self.id} users={self.users}>"
