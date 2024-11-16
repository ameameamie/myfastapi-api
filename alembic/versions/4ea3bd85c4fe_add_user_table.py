"""add user table

Revision ID: 4ea3bd85c4fe
Revises: f143fdd8764c
Create Date: 2024-11-15 18:58:06.267281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ea3bd85c4fe'
down_revision: Union[str, None] = 'f143fdd8764c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column(
            'created_at', 
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
            ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade() -> None:
    op.drop_table('users')
