import uuid
from typing import Annotated

from fastapi_users import schemas
from annotated_types import Len


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    password: Annotated[str, Len(min_length=8)]


class UserUpdate(schemas.BaseUserUpdate):
    password: Annotated[str, Len(min_length=8)]
