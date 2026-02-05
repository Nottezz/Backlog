from fastapi import APIRouter

from backlog_app.dependencies.authentification.fastapi_users_routers import (
    fastapi_users,
)
from backlog_app.schemas.user import UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate))
