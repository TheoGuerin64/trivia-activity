import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta

from .settings import POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_USER

engine = sqlalchemy.create_engine(
    sqlalchemy.URL.create(
        "postgresql+psycopg2",
        username=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database=POSTGRES_DB,
        host="server-db",
        port=5432,
    )
)
Session = sessionmaker(bind=engine)
Base: DeclarativeMeta = declarative_base()
