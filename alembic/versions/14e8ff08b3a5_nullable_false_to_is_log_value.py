"""nullable false to is_log_value

Revision ID: 14e8ff08b3a5
Revises: 0a93ff296ff5
Create Date: 2024-02-20 09:03:54.533897

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14e8ff08b3a5'
down_revision: Union[str, None] = '0a93ff296ff5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sensor_channel', 'is_log_value',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('sensor_channel', 'is_log_value',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###