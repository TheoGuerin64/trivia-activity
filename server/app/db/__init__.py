import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from ..settings import POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER

engine = create_async_engine(
    sqlalchemy.URL.create(
        "postgresql+asyncpg",
        username=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database=POSTGRES_DB,
        host="server-db",
        port=5432,
    )
)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


async def init_tables():
    from . import schemas  # noqa: F401

    async with engine.begin() as conn:
        if __debug__:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
