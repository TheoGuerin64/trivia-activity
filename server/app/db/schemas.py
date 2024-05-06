from sqlalchemy import CHAR, Boolean, Integer, Select, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    discord_id: Mapped[str] = mapped_column(String(20), index=True, unique=True)
    socket_id: Mapped[str] = mapped_column(CHAR(20), unique=True)
    channel_id: Mapped[str] = mapped_column(String(20))
    connected: Mapped[bool] = mapped_column(Boolean)

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
        return f"<User id={self.id} connected={self.connected}>"
