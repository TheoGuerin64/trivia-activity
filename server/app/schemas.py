from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    sid: Mapped[str]

    def __repr__(self):
        return f"<User {self.sid}>"
