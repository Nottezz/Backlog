import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from models.base import Base
from sqlalchemy import (Boolean, DateTime, Float, ForeignKey, Integer, String,
                        func)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .users import User


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)

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

    watched: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
        nullable=False,
    )

    rating: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    watch_link: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    kp_id: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )

    imdb_id: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )
    user: Mapped["User"] = relationship("User", back_populates="movies")
