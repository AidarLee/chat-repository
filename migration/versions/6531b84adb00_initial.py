"""initial

Revision ID: 6531b84adb00
Revises: 400182c2e8bb
Create Date: 2023-09-08 19:58:05.332247

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6531b84adb00'
down_revision: Union[str, None] = '400182c2e8bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('userchats', sa.Column('message_count', sa.Integer(), nullable=True))


def downgrade() -> None:
    pass
