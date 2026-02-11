from typing import Annotated
from uuid import UUID

from annotated_types import Len
from fastapi_users import schemas
from pydantic import BaseModel, EmailStr, ConfigDict

from .helper import to_camel_case


class UserRead(BaseModel):
    id: UUID
    email: EmailStr

    @property
    def username(self):
        return self.email.split('@')[0]

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel_case
    )


class UserCreate(schemas.BaseUserCreate):
    password: Annotated[str, Len(min_length=8)]


class UserUpdate(schemas.BaseUserUpdate):
    password: Annotated[str, Len(min_length=8)]
