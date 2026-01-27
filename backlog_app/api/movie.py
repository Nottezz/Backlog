from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from backlog_app.schemas.movie import MovieCreate, MovieRead
from backlog_app.crud import movie
from backlog_app.core.database import get_session
from schemas.movie import MovieUpdate

router = APIRouter(prefix="/movies", tags=["Movies"])

@router.post("/", response_model=MovieRead)
async def add_movie(movie_create: MovieCreate, db: AsyncSession = Depends(get_session)):
    return await movie.create_movie(db, movie_create)

@router.get("/", response_model=List[MovieRead])
async def list_movies(db: AsyncSession = Depends(get_session)):
    return await movie.get_movies(db)

@router.put("/", response_model=MovieRead)
async def update_movie(movie_update: MovieUpdate, db: AsyncSession = Depends(get_session)):
    return await movie.update_movie(db, movie_update)

@router.delete("/{id}", response_model=MovieRead)
async def delete_movie(movie_id: int, db: AsyncSession = Depends(get_session)):
    return await movie.delete_movie(db, movie_id)
