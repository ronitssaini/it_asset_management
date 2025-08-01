"""add storage fields to asset model

Revision ID: 9ad583306e89
Revises: 
Create Date: 2025-07-10 12:29:40.548593

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ad583306e89'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assets', sa.Column('total_capacity', sa.String(length=50), nullable=True))
    op.create_unique_constraint(None, 'assets', ['serial_number'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'assets', type_='unique')
    op.drop_column('assets', 'total_capacity')
    # ### end Alembic commands ###
