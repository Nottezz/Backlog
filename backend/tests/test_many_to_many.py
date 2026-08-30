"""Tests for many-to-many movie sharing functionality."""

import pytest
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backlog_app.api import crud
from backlog_app.models import Movie, User
from backlog_app.models.user_movie import UserMovie
from backlog_app.schemas.movie import MovieCreate, MovieUpdate

# ── create_movie: owner UserMovie is auto-created ────────────────────────────


async def test_create_movie_auto_creates_owner_user_movie(
    session: AsyncSession,
    user_test: User,
) -> None:
    movie_in = MovieCreate(title="Auto UserMovie Test", description="A" * 20)
    movie_read = await crud.create_movie(session, movie_in, user_test)

    result = await session.execute(select(Movie).where(Movie.slug == movie_read.slug))
    movie = result.scalars().first()
    assert movie is not None

    um_result = await session.execute(
        select(UserMovie).where(
            UserMovie.user_id == user_test.id,
            UserMovie.movie_id == movie.id,
        )
    )
    user_movie = um_result.scalars().first()
    assert user_movie is not None
    assert user_movie.user_id == user_test.id
    assert user_movie.movie_id == movie.id

    await crud.delete_movie(session, movie_read.slug, user_test)


# ── create_user_movie ─────────────────────────────────────────────────────────


async def test_create_user_movie(
    session: AsyncSession,
    user_other: User,
    published_movie: Movie,
) -> None:
    user_movie = await crud.create_user_movie(
        session, user_other.id, published_movie.id
    )

    assert user_movie.user_id == user_other.id
    assert user_movie.movie_id == published_movie.id
    assert user_movie.watched is False
    assert user_movie.note is None
    assert user_movie.rating is None

    await crud.delete_user_movie(session, user_other.id, published_movie.id)


async def test_create_user_movie_is_idempotent(
    session: AsyncSession,
    user_other: User,
    published_movie: Movie,
) -> None:
    um1 = await crud.create_user_movie(session, user_other.id, published_movie.id)
    um2 = await crud.create_user_movie(session, user_other.id, published_movie.id)
    assert um1.id == um2.id

    await crud.delete_user_movie(session, user_other.id, published_movie.id)


# ── delete_user_movie ─────────────────────────────────────────────────────────


async def test_delete_user_movie(
    session: AsyncSession,
    user_other: User,
    published_movie: Movie,
) -> None:
    await crud.create_user_movie(session, user_other.id, published_movie.id)
    await crud.delete_user_movie(session, user_other.id, published_movie.id)

    um_result = await session.execute(
        select(UserMovie).where(
            UserMovie.user_id == user_other.id,
            UserMovie.movie_id == published_movie.id,
        )
    )
    assert um_result.scalars().first() is None


async def test_delete_user_movie_not_joined_raises_404(
    session: AsyncSession,
    user_other: User,
    published_movie: Movie,
) -> None:
    with pytest.raises(HTTPException) as exc_info:
        await crud.delete_user_movie(session, user_other.id, published_movie.id)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


# ── is_joined flag via get_movie_by_slug ──────────────────────────────────────


async def test_is_joined_false_for_owner(
    session: AsyncSession,
    user_test: User,
    published_movie: Movie,
) -> None:
    movie_read = await crud.get_movie_by_slug(
        session, published_movie.slug, user_test.id
    )
    assert movie_read.is_joined is False


async def test_is_joined_true_for_joined_user(
    session: AsyncSession,
    user_other: User,
    published_movie: Movie,
) -> None:
    await crud.create_user_movie(session, user_other.id, published_movie.id)

    movie_read = await crud.get_movie_by_slug(
        session, published_movie.slug, user_other.id
    )
    assert movie_read.is_joined is True

    await crud.delete_user_movie(session, user_other.id, published_movie.id)


async def test_is_joined_false_for_stranger(
    session: AsyncSession,
    user_other: User,
    published_movie: Movie,
) -> None:
    movie_read = await crud.get_movie_by_slug(
        session, published_movie.slug, user_other.id
    )
    assert movie_read.is_joined is False


# ── partial_update_movie: owner permissions ───────────────────────────────────


async def test_owner_can_update_title(
    session: AsyncSession,
    user_test: User,
    published_movie: Movie,
) -> None:
    updated = await crud.partial_update_movie(
        session, published_movie.slug, MovieUpdate(title="Updated Title"), user_test
    )
    assert updated.title == "Updated Title"


async def test_non_owner_cannot_update_title(
    session: AsyncSession,
    user_other: User,
    published_movie: Movie,
) -> None:
    with pytest.raises(HTTPException) as exc_info:
        await crud.partial_update_movie(
            session, published_movie.slug, MovieUpdate(title="Hacked Title"), user_other
        )
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN


# ── partial_update_movie: joined user personal fields ────────────────────────


async def test_joined_user_can_update_watched(
    session: AsyncSession,
    user_other: User,
    published_movie: Movie,
) -> None:
    await crud.create_user_movie(session, user_other.id, published_movie.id)

    updated = await crud.partial_update_movie(
        session, published_movie.slug, MovieUpdate(watched=True), user_other
    )
    assert updated.watched is True

    await crud.delete_user_movie(session, user_other.id, published_movie.id)


async def test_joined_user_can_update_note(
    session: AsyncSession,
    user_other: User,
    published_movie: Movie,
) -> None:
    await crud.create_user_movie(session, user_other.id, published_movie.id)

    updated = await crud.partial_update_movie(
        session, published_movie.slug, MovieUpdate(note="My note"), user_other
    )
    assert updated.note == "My note"

    await crud.delete_user_movie(session, user_other.id, published_movie.id)


async def test_joined_user_can_update_rating(
    session: AsyncSession,
    user_other: User,
    published_movie: Movie,
) -> None:
    await crud.create_user_movie(session, user_other.id, published_movie.id)

    updated = await crud.partial_update_movie(
        session, published_movie.slug, MovieUpdate(rating=7.5), user_other
    )
    assert updated.rating == 7.5

    await crud.delete_user_movie(session, user_other.id, published_movie.id)


async def test_non_joined_user_cannot_update_personal_fields(
    session: AsyncSession,
    user_other: User,
    published_movie: Movie,
) -> None:
    with pytest.raises(HTTPException) as exc_info:
        await crud.partial_update_movie(
            session, published_movie.slug, MovieUpdate(watched=True), user_other
        )
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN


# ── personal state isolation ──────────────────────────────────────────────────


async def test_personal_state_isolation(
    session: AsyncSession,
    user_test: User,
    user_other: User,
    published_movie: Movie,
) -> None:
    """watched и note хранятся отдельно для каждого пользователя."""
    await crud.partial_update_movie(
        session,
        published_movie.slug,
        MovieUpdate(watched=True, note="Owner note"),
        user_test,
    )

    await crud.create_user_movie(session, user_other.id, published_movie.id)
    await crud.partial_update_movie(
        session,
        published_movie.slug,
        MovieUpdate(note="Other note"),
        user_other,
    )

    owner_view = await crud.get_movie_by_slug(
        session, published_movie.slug, user_test.id
    )
    other_view = await crud.get_movie_by_slug(
        session, published_movie.slug, user_other.id
    )

    assert owner_view.watched is True
    assert owner_view.note == "Owner note"
    assert other_view.watched is False
    assert other_view.note == "Other note"

    await crud.delete_user_movie(session, user_other.id, published_movie.id)


# ── get_movies: is_joined in list ─────────────────────────────────────────────


async def test_get_movies_is_joined_true_for_joined_user(
    session: AsyncSession,
    user_other: User,
    published_movie: Movie,
) -> None:
    await crud.create_user_movie(session, user_other.id, published_movie.id)

    movie_list = await crud.get_movies(
        session,
        filter_user_id=user_other.id,
        current_user_id=user_other.id,
    )

    joined = next(
        (m for m in movie_list.movies if m.slug == published_movie.slug), None
    )
    assert joined is not None
    assert joined.is_joined is True

    await crud.delete_user_movie(session, user_other.id, published_movie.id)


async def test_get_movies_is_joined_false_for_owner(
    session: AsyncSession,
    user_test: User,
    published_movie: Movie,
) -> None:
    movie_list = await crud.get_movies(
        session,
        filter_user_id=user_test.id,
        current_user_id=user_test.id,
    )

    owner_movie = next(
        (m for m in movie_list.movies if m.slug == published_movie.slug), None
    )
    assert owner_movie is not None
    assert owner_movie.is_joined is False


async def test_get_movies_current_user_id_populates_watched(
    session: AsyncSession,
    user_other: User,
    published_movie: Movie,
) -> None:
    """current_user_id всегда загружает личное состояние, даже без filter_user_id."""
    await crud.create_user_movie(session, user_other.id, published_movie.id)
    await crud.partial_update_movie(
        session, published_movie.slug, MovieUpdate(watched=True), user_other
    )

    # public list (filter_user_id=None), but current_user_id set
    movie_list = await crud.get_movies(
        session,
        filter_user_id=None,
        current_user_id=user_other.id,
    )

    movie = next((m for m in movie_list.movies if m.slug == published_movie.slug), None)
    assert movie is not None
    assert movie.watched is True
    assert movie.is_joined is True

    await crud.delete_user_movie(session, user_other.id, published_movie.id)
