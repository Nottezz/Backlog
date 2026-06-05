"""add field note to movie table

Revision ID: d6cf1a127f6c
Revises: 5ee6456bd1f5
Create Date: 2026-06-05 20:16:19.752170

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d6cf1a127f6c"
down_revision: Union[str, Sequence[str], None] = "5ee6456bd1f5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("movies", sa.Column("note", sa.String(length=50), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("movies", "note")
