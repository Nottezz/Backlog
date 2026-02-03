from typing import TYPE_CHECKING, Annotated

from storages.database import get_async_session
from fastapi import Depends
from models import User

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_db(session: Annotated["AsyncSession", Depends(get_async_session)]):
    yield User.get_db(session)
