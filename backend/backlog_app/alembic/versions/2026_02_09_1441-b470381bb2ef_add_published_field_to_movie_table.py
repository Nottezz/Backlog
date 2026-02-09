"""add published field to Movie table

Revision ID: b470381bb2ef
Revises: 38f457e3cf5f
Create Date: 2026-02-09 14:41:50.069806

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "b470381bb2ef"
down_revision: Union[str, Sequence[str], None] = "38f457e3cf5f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "movies",
        sa.Column(
            "published", sa.Boolean(), server_default="false", nullable=False
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("movies", "published")
