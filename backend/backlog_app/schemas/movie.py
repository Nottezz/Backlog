from datetime import datetime
from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel, Field, ConfigDict

from .helper import to_camel_case
from .user import UserRead


class MovieBase(BaseModel):
    title: Annotated[str, Len(min_length=3, max_length=255)]
    description: Annotated[str, Len(min_length=20, max_length=1000)]
    year: int
    rating: float
    watch_link: str | None = None
    kp_id: int | None = None
    imdb_id: int | None = None

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel_case,
        validate_by_name=True,
    )


class MovieCreate(MovieBase):
    description: Annotated[str, Len(min_length=20, max_length=1000)] | None = None
    year: int | None = None
    rating: float | None = Field(default=None, ge=1.0, le=10.0)
    published: bool = False


class MovieUpdate(MovieBase):
    title: Annotated[str, Len(min_length=3, max_length=255)] | None = None
    description: Annotated[str, Len(min_length=20, max_length=1000)] | None = None
    year: int | None = None
    watched: bool | None = None
    rating: float | None = Field(default=None, ge=1.0, le=10.0)
    published: bool = False


class MovieRead(MovieBase):
    id: int
    user: UserRead
    description: Annotated[str, Len(min_length=20, max_length=1000)] | None
    year: int | None
    watched: bool
    rating: float | None
    created_at: datetime

class MovieList(BaseModel):
    movies: list[MovieRead]
