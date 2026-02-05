import uuid
from typing import Annotated

from annotated_types import Len
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    password: Annotated[str, Len(min_length=8)]


class UserUpdate(schemas.BaseUserUpdate):
    password: Annotated[str, Len(min_length=8)]
