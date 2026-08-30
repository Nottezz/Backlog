"""add user_movies table

Revision ID: a1b2c3d4e5f6
Revises: 4dc9128d633a
Create Date: 2026-08-23 00:01:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "4dc9128d633a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Create user_movies table
    op.create_table(
        "user_movies",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("movie_id", sa.Integer(), nullable=False),
        sa.Column("watched", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("note", sa.String(length=50), nullable=True),
        sa.Column("rating", sa.Float(), nullable=True),
        sa.Column(
            "joined_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["movie_id"], ["movies.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "movie_id", name="uq_user_movie"),
    )

    # 2. Migrate existing movie data into user_movies
    op.execute("""
        INSERT INTO user_movies (user_id, movie_id, watched, note, rating, joined_at)
        SELECT user_id, id, watched, note, rating, created_at
        FROM movies
        """)

    # 3. Drop watched, note, rating from movies
    op.drop_column("movies", "watched")
    op.drop_column("movies", "note")
    op.drop_column("movies", "rating")


def downgrade() -> None:
    """Downgrade schema."""
    # 1. Re-add columns to movies
    op.add_column(
        "movies",
        sa.Column("watched", sa.Boolean(), server_default="false", nullable=False),
    )
    op.add_column(
        "movies",
        sa.Column("note", sa.String(length=50), nullable=True),
    )
    op.add_column(
        "movies",
        sa.Column("rating", sa.Float(), nullable=True),
    )

    # 2. Restore data from user_movies (owner's row)
    op.execute("""
        UPDATE movies
        SET
            watched = um.watched,
            note = um.note,
            rating = um.rating
        FROM user_movies um
        WHERE um.movie_id = movies.id
          AND um.user_id = movies.user_id
        """)

    # 3. Drop user_movies table
    op.drop_table("user_movies")
