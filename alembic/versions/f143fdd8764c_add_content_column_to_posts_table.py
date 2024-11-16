"""add  content column to posts table

Revision ID: f143fdd8764c
Revises: eacc2be2e49e
Create Date: 2024-11-15 18:52:20.583271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f143fdd8764c'
down_revision: Union[str, None] = 'eacc2be2e49e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_column('posts', 'content')
