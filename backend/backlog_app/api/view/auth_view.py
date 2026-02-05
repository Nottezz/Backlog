from fastapi import APIRouter

from backlog_app.dependencies.authentification.backend import authentication_backend
from backlog_app.dependencies.authentification.fastapi_users_routers import (
    fastapi_users,
)
from backlog_app.schemas.user import UserCreate, UserRead

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)
# /login /logout
router.include_router(
    fastapi_users.get_auth_router(
        authentication_backend,
        # requires_verification=True,  # It is not necessary to include the parameter in this application.
    )
)

# /register
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))

# /request-verify-token /verify
router.include_router(fastapi_users.get_verify_router(UserRead))

# /forgot-password # /reset-password
router.include_router(fastapi_users.get_reset_password_router())
