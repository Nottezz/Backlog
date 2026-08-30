import random as stdlib_random
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backlog_app.api import crud
from backlog_app.dependencies.authentification.fastapi_users_routers import (
    current_active_user,
)
from backlog_app.models.movie import Movie
from backlog_app.models.user_movie import UserMovie
from backlog_app.models.users import User
from backlog_app.schemas.movie import MovieCreate, MovieList, MovieRead, MovieUpdate
from backlog_app.storages.database import get_async_session
from backlog_app.tasks.movie_task import update_movie_metadata

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.post("/", response_model=MovieRead, status_code=status.HTTP_201_CREATED)
async def add_movie(
    movie_create: MovieCreate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(current_active_user)],
    background_tasks: BackgroundTasks,
):
    movie = await crud.create_movie(db, movie_create, user=user)
    background_tasks.add_task(update_movie_metadata, movie.slug, user.id)
    return movie


@router.get("/", response_model=MovieList)
async def get_movie_list(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(current_active_user)],
    only_mine: bool = False,
):
    filter_user_id = user.id if only_mine else None
    movies = await crud.get_movies(
        db, filter_user_id=filter_user_id, current_user_id=user.id
    )
    return movies


@router.get("/random", response_model=MovieRead)
async def get_random_movie(
    db: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(current_active_user)],
    exclude_ids: list[int] = Query(default=[]),
):
    pool = await crud.get_random_movie_pool(db, user.id, exclude_ids)

    if not pool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No unwatched movies available",
        )

    chosen = stdlib_random.choice(pool)
    return await crud.get_movie_by_slug(db, chosen.slug, user.id)


@router.get("/{slug}", response_model=MovieRead)
async def get_movie_by_slug(
    slug: str,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(current_active_user)],
):
    return await crud.get_movie_by_slug(db, slug, user.id)


@router.post("/{slug}/join", response_model=MovieRead)
async def join_movie(
    slug: str,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(current_active_user)],
):
    # 1. Find movie (no user_id filter)
    result = await db.execute(select(Movie).where(Movie.slug == slug))
    movie = result.scalars().first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # 2. Must be published to join
    if not movie.published:
        raise HTTPException(status_code=403, detail="Cannot join an unpublished movie")

    # 3. Owner cannot join their own movie
    if movie.user_id == user.id:
        raise HTTPException(status_code=400, detail="You cannot join your own movie")

    # 4. Check if already joined
    existing_result = await db.execute(
        select(UserMovie).where(
            UserMovie.user_id == user.id,
            UserMovie.movie_id == movie.id,
        )
    )
    if existing_result.scalars().first():
        raise HTTPException(status_code=409, detail="Already joined this movie")

    # 5. Create UserMovie
    await crud.create_user_movie(db, user.id, movie.id)
    await db.commit()

    # 6. Return updated MovieRead
    return await crud.get_movie_by_slug(db, slug, user.id)


@router.delete("/{slug}/join", status_code=status.HTTP_204_NO_CONTENT)
async def leave_movie(
    slug: str,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(current_active_user)],
):
    # 1. Find movie
    result = await db.execute(select(Movie).where(Movie.slug == slug))
    movie = result.scalars().first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # 2. Owner cannot leave their own movie
    if movie.user_id == user.id:
        raise HTTPException(status_code=400, detail="You cannot leave your own movie")

    # 3. Delete UserMovie (raises 404 if not found)
    await crud.delete_user_movie(db, user.id, movie.id)
    await db.commit()


@router.put("/{slug}", response_model=MovieRead)
async def update_movie(
    slug: str,
    movie_update: MovieUpdate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(current_active_user)],
):
    return await crud.update_movie(db, slug, movie_update, user)


@router.patch("/{slug}", response_model=MovieRead)
async def partial_update_movie(
    slug: str,
    movie_update: MovieUpdate,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(current_active_user)],
):
    return await crud.partial_update_movie(db, slug, movie_update, user)


@router.delete(
    "/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_movie(
    slug: str,
    db: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[User, Depends(current_active_user)],
):
    return await crud.delete_movie(db, slug, user)
