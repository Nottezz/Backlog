"""add fields for imdb rating

Revision ID: 5ee6456bd1f5
Revises: b470381bb2ef
Create Date: 2026-03-03 16:07:42.108873

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5ee6456bd1f5"
down_revision: Union[str, Sequence[str], None] = "b470381bb2ef"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("movies", sa.Column("imdb_rating", sa.Float(), nullable=True))
    op.add_column("movies", sa.Column("metacritic_score", sa.Float(), nullable=True))
    op.drop_column("movies", "kp_id")
    op.drop_column("movies", "imdb_id")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "movies",
        sa.Column("imdb_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "movies",
        sa.Column("kp_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.drop_column("movies", "metacritic_score")
    op.drop_column("movies", "imdb_rating")
