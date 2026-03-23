import logging

from sqlalchemy.ext.asyncio import AsyncSession

from backlog_app.api import crud
from backlog_app.api.crud import partial_update_movie
from backlog_app.config import settings
from backlog_app.models import User
from backlog_app.schemas.movie import MovieRead, MovieUpdate
from backlog_app.servicies.ai_agent import TranslationService
from backlog_app.servicies.imdb_api.provider import IMDBProvider

logger = logging.getLogger(__name__)

provider = IMDBProvider(base_url=settings.imdb_url)
translator = TranslationService()


async def update_movie_rating(movie: MovieRead, db: AsyncSession, user: User):
    movie_db = await crud.get_movie_by_id(db, movie.id)
    year = getattr(movie, "year", None)

    if year is None:
        logger.info("Movie <%s> has no year, skipping rating update", movie.id)
        return

    try:
        imdb_rating, metacritic_score = await provider.get_title_rating(
            movie_db.title, movie_db.year
        )
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


async def update_movie_description(
    movie: MovieRead, db: AsyncSession, user: User
) -> None:

    movie_db = await crud.get_movie_by_id(db, movie.id)

    description = getattr(movie_db, "description", None)
    year = getattr(movie_db, "year", None)

    if description and description.strip():
        logger.info("Movie <%s> already has description, skipping", movie.id)
        return

    if not year:
        logger.info("Movie <%s> has no year, skipping description update", movie.id)
        return

    try:
        en_description = await provider.get_title_description(
            movie_db.title, movie_db.year
        )
    except Exception as e:
        logger.error("Failed to fetch description for movie <%s>: %s", movie.id, e)
        return

    try:
        ru_description = await translator.translate(en_description)
    except Exception as e:
        logger.error("Failed to translate description for movie <%s>: %s", movie.id, e)
        return

    await partial_update_movie(
        db,
        movie.id,
        MovieUpdate(description=ru_description),
        user,
    )

    logger.info("Movie <%s> description updated in background", movie.id)
