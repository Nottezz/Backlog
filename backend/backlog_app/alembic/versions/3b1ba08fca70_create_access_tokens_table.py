"""create access_tokens table

Revision ID: 3b1ba08fca70
Revises: 2c6bd7e56b3f
Create Date: 2026-01-28 11:42:51.989698

"""

from typing import Sequence, Union

import fastapi_users_db_sqlalchemy
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3b1ba08fca70"
down_revision: Union[str, Sequence[str], None] = "2c6bd7e56b3f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "accesstoken",
        sa.Column(
            "user_id", fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False
        ),
        sa.Column("token", sa.String(length=43), nullable=False),
        sa.Column(
            "created_at",
            fastapi_users_db_sqlalchemy.generics.TIMESTAMPAware(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("token"),
    )
    op.create_index(
        op.f("ix_accesstoken_created_at"), "accesstoken", ["created_at"], unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_accesstoken_created_at"), table_name="accesstoken")
    op.drop_table("accesstoken")
