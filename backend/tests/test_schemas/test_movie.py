from datetime import datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from backlog_app.schemas.movie import MovieCreate, MovieRead, MovieUpdate
from backlog_app.schemas.user import UserRead


def test_movie_can_be_create_from_create_schema() -> None:
    movie_in = MovieCreate(
        title="Test Movie",
        description="Test Movie Description",
        watch_link="https://example.com",
        rating=6.7,
    )
    user = UserRead(id=uuid4(), email="test@example.com")
    movie = MovieRead(
        **movie_in.model_dump(),
        id=0,
        watched=False,
        created_at=datetime.now(),
        user=user,
    )

    assert movie_in.title == movie.title
    assert movie_in.description == movie.description
    assert movie_in.watch_link == movie.watch_link
    assert movie_in.rating == movie.rating


@pytest.mark.parametrize(
    ("title", "description", "should_raise"),
    [
        pytest.param("a", "a" * 18, True, id="values-less-than-min"),
        pytest.param("a" * 3, "a" * 20, False, id="minimum-values"),
        pytest.param("a" * 255, "a" * 1000, False, id="maximum-values"),
        pytest.param("a" * 300, "a" * 1500, True, id="values-higher-than-max"),
    ],
)
def test_movie_create_max_value(
    title: str, description: str, should_raise: bool
) -> None:
    if should_raise:
        with pytest.raises(ValidationError):
            MovieCreate(
                title=title,
                description=description,
            )
    else:
        movie_in = MovieCreate(
            title=title,
            description=description,
        )
        user = UserRead(id=uuid4(), email="test@example.com")
        movie = MovieRead(
            **movie_in.model_dump(),
            id=0,
            watched=False,
            created_at=datetime.now(),
            user=user,
        )

        assert movie.title == title
        assert movie.description == description


def test_movie_update_from_update_schema() -> None:
    user = UserRead(id=uuid4(), email="test@example.com")

    movie = MovieRead(
        id=0,
        user=user,
        title="Test Movie",
        description="Test Movie Description",
        watch_link="https://example.com",
        watched=True,
        created_at=datetime.now(),
        imdb_id=1234,
        kp_id=5678,
        year=2020,
        rating=2.8,
    )
    movie_update = MovieUpdate(
        title="Test Movie Update",
        description="Test Movie Update Description",
        watch_link="https://abc.example.com",
    )
    for field, value in movie_update.model_dump(exclude_unset=True).items():
        setattr(movie, field, value)

    assert movie_update.title == movie.title
    assert movie_update.description == movie.description
    assert movie_update.watch_link == movie.watch_link
