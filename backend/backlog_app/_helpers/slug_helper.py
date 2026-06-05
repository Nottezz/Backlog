from models import Movie
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def generate_unique_slug(db: AsyncSession, title: str) -> str:
    base_slug = slugify(title)

    slug = base_slug
    counter = 1

    while True:
        query = select(Movie).where(Movie.slug == slug)
        result = await db.execute(query)

        if result.scalar_one_or_none() is None:
            return slug

        slug = f"{base_slug}-{counter}"
        counter += 1
