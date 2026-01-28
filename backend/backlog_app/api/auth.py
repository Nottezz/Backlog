from fastapi import APIRouter

from dependencies.authentification.fastapi_users_routers import fastapi_users
from dependencies.authentification.backend import authentication_backend

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)
router.include_router(
    fastapi_users.get_auth_router(authentication_backend))
