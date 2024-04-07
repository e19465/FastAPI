"""create likes table

Revision ID: 4635e5a6657f
Revises: a94aad86d43b
Create Date: 2024-04-07 08:58:10.428085

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4635e5a6657f'
down_revision: Union[str, None] = 'a94aad86d43b'
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
