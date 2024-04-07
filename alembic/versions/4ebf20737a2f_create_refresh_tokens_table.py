"""create refresh_tokens table

Revision ID: 4ebf20737a2f
Revises: 4635e5a6657f
Create Date: 2024-04-07 08:59:38.597869

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ebf20737a2f'
down_revision: Union[str, None] = '4635e5a6657f'
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
