from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated

from dependencies.authentification.fastapi_users_routers import current_active_user
from schemas.movie import MovieCreate, MovieRead
from models.users import User
from crud import movie
from core.database import get_async_session
from schemas.movie import MovieUpdate

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.post("/", response_model=MovieRead)
async def add_movie(
    movie_create: MovieCreate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(current_active_user)],
):
    return await movie.create_movie(db, movie_create)


@router.get("/", response_model=List[MovieRead])
async def list_movies(
    db: Annotated[AsyncSession, Depends(get_async_session)],
):
    return await movie.get_movies(db)


@router.get("/{movie_id}", response_model=MovieRead)
async def get_movie_by_id(movie_id: int, db: Annotated[AsyncSession, Depends(get_async_session)],
                          user: Annotated[User, Depends(current_active_user)], ):
    return await movie.get_movie_by_id(db, movie_id)


@router.put("/{movie_id}", response_model=MovieRead)
async def update_movie(
    movie_id: int,
    movie_update: MovieUpdate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(current_active_user)],
):
    return await movie.update_movie(db, movie_id, movie_update)


@router.patch("/{movie_id}", response_model=MovieRead)
async def partial_update_movie(
    movie_id: int,
    movie_update: MovieUpdate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(current_active_user)],
):
    return await movie.partial_update_movie(db, movie_id, movie_update)


@router.delete("/{movie_id}", response_model=MovieRead)
async def delete_movie(movie_id: int, db: Annotated[AsyncSession, Depends(get_async_session)],
                       user: Annotated[User, Depends(current_active_user)], ):
    return await movie.delete_movie(db, movie_id)
