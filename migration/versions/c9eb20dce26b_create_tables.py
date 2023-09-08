"""Create tables

Revision ID: c9eb20dce26b
Revises: adbecffbfccd
Create Date: 2023-09-08 18:18:09.865901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9eb20dce26b'
down_revision: Union[str, None] = 'adbecffbfccd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
