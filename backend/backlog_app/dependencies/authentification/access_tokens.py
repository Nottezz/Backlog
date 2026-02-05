from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from backlog_app.models import AccessToken
from backlog_app.storages.database import get_async_session

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_token_db(
    session: Annotated["AsyncSession", Depends(get_async_session)],
):
    yield AccessToken.get_db(session)
