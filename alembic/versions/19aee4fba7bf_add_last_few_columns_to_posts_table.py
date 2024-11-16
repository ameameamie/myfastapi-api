"""add last few columns to posts table

Revision ID: 19aee4fba7bf
Revises: b7e74183a5f5
Create Date: 2024-11-16 05:38:21.573311

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19aee4fba7bf'
down_revision: Union[str, None] = 'b7e74183a5f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('visible', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))


def downgrade() -> None:
    op.drop_column('posts', 'visible')
    op.drop_column('posts', 'created_at')
