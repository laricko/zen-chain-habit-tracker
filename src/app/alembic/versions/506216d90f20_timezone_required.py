"""timezone_required

Revision ID: 506216d90f20
Revises: d063b92306e3
Create Date: 2025-04-23 23:51:56.142679

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '506216d90f20'
down_revision: Union[str, None] = 'd063b92306e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'timezone',
               existing_type=sa.VARCHAR(length=31),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'timezone',
               existing_type=sa.VARCHAR(length=31),
               nullable=True)
    # ### end Alembic commands ###
