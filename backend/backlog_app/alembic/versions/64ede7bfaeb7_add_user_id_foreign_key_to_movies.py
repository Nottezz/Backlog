"""add user_id foreign key to movies

Revision ID: 64ede7bfaeb7
Revises: 7399ea42770f
Create Date: 2026-01-30 14:27:53.993500

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "64ede7bfaeb7"
down_revision: Union[str, Sequence[str], None] = "7399ea42770f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("movies", sa.Column("user_id", sa.UUID(), nullable=False))
    op.create_foreign_key(None, "movies", "user", ["user_id"], ["id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "movies", type_="foreignkey")
    op.drop_column("movies", "user_id")
