from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
from sqlalchemy.orm import Mapped, relationship

from .base import Base

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from .movie import Movie
    from .user_movie import UserMovie


class User(SQLAlchemyBaseUserTableUUID, Base):
    movies: Mapped[list["Movie"]] = relationship("Movie", back_populates="user")
    joined_movies: Mapped[list["UserMovie"]] = relationship(
        "UserMovie", back_populates="user"
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
