"""add foreign-key to posts table

Revision ID: b7e74183a5f5
Revises: 4ea3bd85c4fe
Create Date: 2024-11-15 19:31:17.301956

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7e74183a5f5'
down_revision: Union[str, None] = '4ea3bd85c4fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('author_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'posts_users_fkey', 
        source_table='posts',
        referent_table='users',
        local_cols=['author_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
        )


def downgrade() -> None:
    op.drop_constraint('posts_users_fkey', table_name='posts')
    op.drop_column('posts', 'author_id')
