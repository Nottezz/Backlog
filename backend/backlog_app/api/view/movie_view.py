from typing import Annotated, List

from api import crud
from dependencies.authentification.fastapi_users_routers import current_active_user
from fastapi import APIRouter, Depends
from models.users import User
from schemas.movie import MovieCreate, MovieRead, MovieUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from storages.database import get_async_session

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.post("/", response_model=MovieRead)
async def add_movie(
    movie_create: MovieCreate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(current_active_user)],
):
    return await crud.create_movie(db, movie_create, user=user)


@router.get("/", response_model=List[MovieRead])
async def list_movies(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(current_active_user)],
    only_mine: bool = False,
):
    user_id = user.id if only_mine else None
    movies = await crud.get_movies(db, user_id=user_id)
    return movies


@router.get("/{movie_id}", response_model=MovieRead)
async def get_movie_by_id(
    movie_id: int,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(current_active_user)],
    only_mine: bool = False,
):
    user_id = user.id if only_mine else None
    one_movie = await crud.get_movie_by_id(db, movie_id, user_id)
    return one_movie


@router.put("/{movie_id}", response_model=MovieRead)
async def update_movie(
    movie_id: int,
    movie_update: MovieUpdate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(current_active_user)],
):
    return await crud.update_movie(db, movie_id, movie_update, user)


@router.patch("/{movie_id}", response_model=MovieRead)
async def partial_update_movie(
    movie_id: int,
    movie_update: MovieUpdate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(current_active_user)],
):
    return await crud.partial_update_movie(db, movie_id, movie_update)


@router.delete("/{movie_id}", response_model=MovieRead)
async def delete_movie(
    movie_id: int,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(current_active_user)],
):
    return await crud.delete_movie(db, movie_id, user)
