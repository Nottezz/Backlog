from datetime import datetime

from pydantic import BaseModel, Field


class MovieBase(BaseModel):
    title: str
    description: str
    year: int
    rating: float
    watch_link: str | None = None
    kp_id: int | None = None
    imdb_id: int | None = None


class MovieCreate(MovieBase):
    title: str
    description: str | None = None
    year: int | None = None
    rating: float | None = Field(default=None, ge=1.0, le=10.0)


class MovieUpdate(MovieBase):
    title: str | None = None
    description: str | None = None
    year: int | None = None
    watched: bool | None = None
    rating: float | None = Field(default=None, ge=1.0, le=10.0)


class MovieRead(MovieBase):
    id: int
    user: str
    description: str | None
    year: int | None
    watched: bool
    rating: float | None
    kp_id: int | None = None
    imdb_id: int | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
