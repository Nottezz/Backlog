"""add slug to movie table

Revision ID: 4dc9128d633a
Revises: d6cf1a127f6c
Create Date: 2026-06-05 21:56:00.239241

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4dc9128d633a"
down_revision: Union[str, Sequence[str], None] = "d6cf1a127f6c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("movies", sa.Column("slug", sa.String(length=255), nullable=False))
    op.create_index(op.f("ix_movies_slug"), "movies", ["slug"], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_movies_slug"), table_name="movies")
    op.drop_column("movies", "slug")
