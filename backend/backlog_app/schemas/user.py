from typing import Annotated
from uuid import UUID

from annotated_types import Len
from fastapi_users import schemas
from pydantic import BaseModel, ConfigDict, EmailStr, computed_field

from .helper import to_camel_case


class UserRead(BaseModel):
    id: UUID
    email: EmailStr

    @computed_field
    @property
    def username(self) -> str:
        return self.email.split("@")[0]

    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel_case)


class UserCreate(schemas.BaseUserCreate):
    password: Annotated[str, Len(min_length=8)]


class UserUpdate(schemas.BaseUserUpdate):
    password: Annotated[str, Len(min_length=8)]
