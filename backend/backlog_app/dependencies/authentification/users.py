from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from backlog_app.models import User
from backlog_app.storages.database import get_async_session

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_db(session: Annotated["AsyncSession", Depends(get_async_session)]):
    yield User.get_db(session)
