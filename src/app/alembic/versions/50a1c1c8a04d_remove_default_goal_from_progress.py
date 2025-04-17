"""Remove_default_goal_from_progress

Revision ID: 50a1c1c8a04d
Revises: fb54ce9cd79f
Create Date: 2025-04-17 03:05:36.171629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50a1c1c8a04d'
down_revision: Union[str, None] = 'fb54ce9cd79f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column(
        'progress',
        'goal',
        server_default=None,
    )

def downgrade():
    op.alter_column(
        'progress',
        'goal',
        server_default=sa.text("100"),  # Change this to the original default if different
    )