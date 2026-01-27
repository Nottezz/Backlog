"""initial movies table

Revision ID: 6748dfb93f41
Revises:
Create Date: 2026-01-27 12:03:24.572198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6748dfb93f41'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('movies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=1000), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('watched', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('original_link', sa.String(length=255), nullable=True),
    sa.Column('kp_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_movies_title'), 'movies', ['title'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_movies_title'), table_name='movies')
    op.drop_table('movies')
