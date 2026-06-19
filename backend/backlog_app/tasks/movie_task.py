import logging
from uuid import UUID

from sqlalchemy import select

from backlog_app.api import crud
from backlog_app.api.crud import partial_update_movie
from backlog_app.config import settings
from backlog_app.models.users import User as UserModel
from backlog_app.schemas.movie import MovieUpdate
from backlog_app.servicies.ai_agent import TranslationService
from backlog_app.servicies.imdb_api.provider import IMDBProvider
from backlog_app.storages.database import AsyncSessionLocal

logger = logging.getLogger(__name__)

provider = IMDBProvider(base_url=settings.imdb_url)
translator = TranslationService()


async def update_movie_metadata(
    movie_slug: str,
    user_id: UUID,
) -> None:
    async with AsyncSessionLocal() as db:
        movie = await crud.get_movie_by_slug(
            db,
            movie_slug,
        )

        user_result = await db.execute(select(UserModel).where(UserModel.id == user_id))
        user = user_result.scalars().first()

        if user is None:
            logger.warning("User <%s> not found", user_id)
            return

        if movie is None:
            logger.warning(
                "Movie <%s> not found",
                movie_slug,
            )
            return

        if not movie.year:
            logger.info(
                "Movie <%s> has no year, skipping metadata update",
                movie_slug,
            )
            return

        try:
            title_data = await provider.get_title(
                movie.title,
                movie.year,
            )
        except Exception:
            logger.exception(
                "Failed to fetch imdb data for movie <%s>",
                movie_slug,
            )
            return

        update_data: dict = {}

        rating = title_data.get("rating", {})
        metacritic = title_data.get("metacritic", {})

        update_data["imdb_rating"] = rating.get("aggregateRating")
        update_data["metacritic_score"] = metacritic.get("score")

        if not movie.description:
            description = title_data.get("plot")

            if description:
                try:
                    update_data["description"] = await translator.translate(description)
                except Exception:
                    logger.exception(
                        "Failed to translate description for movie <%s>",
                        movie_slug,
                    )

        if not update_data:
            return

        await partial_update_movie(
            db,
            movie_slug,
            MovieUpdate(**update_data),
            user,
        )

        logger.info(
            "Movie <%s> metadata updated",
            movie_slug,
        )
