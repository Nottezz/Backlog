"""edit field rating, add new field watch_link

Revision ID: 7399ea42770f
Revises: 3b1ba08fca70
Create Date: 2026-01-30 14:18:48.954209

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '7399ea42770f'
down_revision: Union[str, Sequence[str], None] = '3b1ba08fca70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('movies', sa.Column('watch_link', sa.String(length=255), nullable=True))
    op.alter_column('movies', 'rating',
                    existing_type=sa.INTEGER(),
                    type_=sa.Float(),
                    existing_nullable=True)


def downgrade() -> None:
    op.alter_column('movies', 'rating',
                    existing_type=sa.Float(),
                    type_=sa.INTEGER(),
                    existing_nullable=True)
    op.drop_column('movies', 'watch_link')
