from typing import TYPE_CHECKING, Annotated

from core.database import get_async_session
from fastapi import Depends
from models import AccessToken

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_token_db(
    session: Annotated["AsyncSession", Depends(get_async_session)],
):
    yield AccessToken.get_db(session)
