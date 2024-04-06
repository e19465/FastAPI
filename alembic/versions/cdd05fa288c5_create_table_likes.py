"""create table likes

Revision ID: cdd05fa288c5
Revises: 738ed03a69dc
Create Date: 2024-04-06 22:56:51.146938

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cdd05fa288c5'
down_revision: Union[str, None] = '738ed03a69dc'
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

