import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user_movie import UserMovie
    from .users import User


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)

    # todo: подумать на тему составного уникального индекса
    # если фильмы принадлежат разным пользователям, то глобальный unique=True может оказаться лишним.
    slug: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        default="",
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    year: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    published: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
        nullable=False,
    )

    imdb_rating: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    metacritic_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    watch_link: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID, ForeignKey("user.id"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="movies", lazy="joined")
    joined_by_users: Mapped[list["UserMovie"]] = relationship(
        "UserMovie",
        back_populates="movie",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
