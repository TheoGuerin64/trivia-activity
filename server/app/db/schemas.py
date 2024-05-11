from sqlalchemy import CHAR, BigInteger, ForeignKey, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    discord_id: Mapped[int] = mapped_column(BigInteger, index=True, unique=True)

    room_users: Mapped[list["RoomUser"]] = relationship(
        "RoomUser", back_populates="user", passive_deletes=True
    )

    def __init__(self, discord_id: int) -> None:
        super().__init__(discord_id=discord_id)

    @staticmethod
    async def get(session: AsyncSession, id: int) -> "User":
        """Raises `NoResultFound` if the result returns no rows."""
        return await session.get_one(User, id)

    @staticmethod
    async def get_by_discord_id(session: AsyncSession, discord_id: int) -> "User":
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

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id", ondelete="CASCADE"), primary_key=True
    )
    socket_id: Mapped[str] = mapped_column(CHAR(20), unique=True)
    connected: Mapped[bool] = mapped_column(default=True)

    user: Mapped["User"] = relationship("User", back_populates="room_users")
    room: Mapped["Room"] = relationship("Room", back_populates="room_users")

    def __init__(
        self, room_id: int, user_id: int, socket_id: str, connected: bool | None = None
    ) -> None:
        super().__init__(room_id=room_id, user_id=user_id, socket_id=socket_id, connected=connected)

    @staticmethod
    async def get(session: AsyncSession, room_id: int, user_id: int) -> "RoomUser":
        """Raises `NoResultFound` if the result returns no rows."""
        return await session.get_one(RoomUser, (room_id, user_id))

    def __repr__(self) -> str:
        return f"<RoomUser room_id={self.room_id} user_id={self.user_id}>"


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    channel_id: Mapped[int] = mapped_column(BigInteger, index=True, unique=True)

    room_users: Mapped[list["RoomUser"]] = relationship(
        "RoomUser", back_populates="room", passive_deletes=True
    )

    def __init__(self, channel_id: int) -> None:
        super().__init__(channel_id=channel_id)

    @staticmethod
    async def get(session: AsyncSession, id: int) -> "Room":
        """Raises `NoResultFound` if the result returns no rows."""
        return await session.get_one(Room, id)

    @staticmethod
    async def get_by_channel_id(session: AsyncSession, channel_id: int) -> "Room":
        """
        Raises `NoResultFound` if the result returns no rows,
        or `MultipleResultsFound` if multiple rows would be returned.
        """
        statement = Select(Room).where(Room.channel_id == channel_id)
        result = await session.execute(statement)
        return result.scalar_one()

    def __repr__(self) -> str:
        return f"<Room id={self.id}>"
