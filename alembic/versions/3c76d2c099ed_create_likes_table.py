"""create likes table

Revision ID: 3c76d2c099ed
Revises: 3cd5055375dd
Create Date: 2024-04-07 04:40:17.448793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c76d2c099ed'
down_revision: Union[str, None] = '3cd5055375dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        'likes',
        sa.Column('post_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True, nullable=False),
        sa.Column('user_id', sa.dialects.postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    )

def downgrade():
    op.drop_table('likes')
