from pydantic import BaseModel, Field, AnyHttpUrl
from datetime import datetime

class MovieBase(BaseModel):
    title: str
    description: str
    year: int
    rating: float
    original_link: str | None = None
    kp_id: int | None = None

class MovieCreate(MovieBase):
    title: str
    description: str | None = None
    year: int | None = None
    rating: int | None = Field(default=None, ge=1, le=10)


class MovieUpdate(MovieBase):
    title: str | None = None
    description: str | None = None
    year: int | None = None
    watched: bool | None = None
    rating: int | None = Field(default=None, ge=1, le=10)


class MovieRead(BaseModel):
    id: int
    title: str
    description: str | None
    year: int | None
    watched: bool
    rating: int | None
    created_at: datetime

    model_config = {"from_attributes": True}
