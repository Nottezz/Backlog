from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
from models.base import Base
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from .movie import Movie


class User(SQLAlchemyBaseUserTableUUID, Base):
    movies: Mapped[list["Movie"]] = relationship("Movie", back_populates="user")

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
