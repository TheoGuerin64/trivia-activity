from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    discord_id: Mapped[str] = mapped_column(index=True, unique=True)
    socket_id: Mapped[str] = mapped_column(unique=True)
    channel_id: Mapped[str] = mapped_column()
    connected: Mapped[bool] = mapped_column()

    @staticmethod
    async def create(session: AsyncSession, **columns) -> "User":
        user = User(**columns)
        session.add(user)
        return user

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

    def __repr__(self):
        return f"<User id={self.id} discord_id={self.discord_id} socket_id={self.socket_id} channel_id={self.channel_id} connected={self.connected}>"
