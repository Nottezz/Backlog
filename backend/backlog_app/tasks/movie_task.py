import logging

from sqlalchemy.ext.asyncio import AsyncSession

from backlog_app.api.crud import partial_update_movie
from backlog_app.config import settings
from backlog_app.models import User
from backlog_app.schemas.movie import MovieRead, MovieUpdate
from backlog_app.servicies.imdb_api.provider import IMDBProvider
from backlog_app.storages.database import get_async_session

logger = logging.getLogger(__name__)


async def update_movie_rating(movie: MovieRead, db: AsyncSession, user: User):
    provider = IMDBProvider(base_url=settings.imdb_url)

    year = getattr(movie, "year", None)

    if year is None:
        logger.info("Movie <%s> has no year, skipping rating update", movie.id)
        return

    try:
        imdb_rating, metacritic_score = await provider.get_title_rating(movie.title)
    except Exception as e:
        logger.error("Failed to fetch rating for movie <%s>: %s", movie.id, e)
        return

    await partial_update_movie(
        db,
        movie.id,
        MovieUpdate(
            imdb_rating=imdb_rating,
            metacritic_score=metacritic_score,
        ),
        user,
    )

    logger.info("Movie <%s> ratings updated in background", movie.id)
