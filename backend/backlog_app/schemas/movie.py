from datetime import datetime
from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel, ConfigDict, Field

from .helper import to_camel_case
from .user import UserRead


class MovieBase(BaseModel):
    title: Annotated[str, Len(min_length=3, max_length=255)]
    description: Annotated[str, Len(min_length=20, max_length=1000)]
    year: int
    watch_link: str | None = None
    imdb_rating: float | None = None
    metacritic_score: float | None = None
    published: bool = False

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel_case,
        validate_by_name=True,
    )


class MovieCreate(MovieBase):
    description: Annotated[str, Len(min_length=20, max_length=1000)] | None = None
    year: int | None = None
    watched: bool = False
    note: Annotated[str, Len(min_length=2, max_length=50)] | None = None
    rating: float | None = Field(default=None, ge=1.0, le=10.0)


class MovieUpdate(MovieBase):
    title: Annotated[str, Len(min_length=3, max_length=255)] | None = None
    description: Annotated[str, Len(min_length=20, max_length=1000)] | None = None
    year: int | None = None
    watched: bool | None = None
    note: Annotated[str, Len(min_length=2, max_length=50)] | None = None
    rating: float | None = Field(default=None, ge=1.0, le=10.0)


class MovieRead(MovieBase):
    slug: str
    user: UserRead
    description: Annotated[str, Len(min_length=20, max_length=1000)] | None
    year: int | None
    watched: bool = False
    note: str | None = None
    rating: float | None = None
    created_at: datetime
    is_joined: bool = False
    joined_by: list[UserRead] = []


class MovieList(BaseModel):
    movies: list[MovieRead]
