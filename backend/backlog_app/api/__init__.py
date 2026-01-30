from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from .auth_view import router as auth_router
from .movie_view import router as movie_router
from .users_view import router as users_router

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(prefix="/api", dependencies=[Depends(http_bearer)])
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(movie_router)
