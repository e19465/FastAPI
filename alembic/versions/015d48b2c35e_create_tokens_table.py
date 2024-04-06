"""create tokens table

Revision ID: 015d48b2c35e
Revises: cdd05fa288c5
Create Date: 2024-04-06 23:00:26.611205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '015d48b2c35e'
down_revision: Union[str, None] = 'cdd05fa288c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'refresh_tokens',
        sa.Column('id', sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('token', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )

def downgrade():
    op.drop_table('refresh_tokens')
