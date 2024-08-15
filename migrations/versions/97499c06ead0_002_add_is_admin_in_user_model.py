"""002_add_is_admin_in_user_model

Revision ID: 97499c06ead0
Revises: e841c8bb5871
Create Date: 2024-08-12 23:00:30.448979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97499c06ead0'
down_revision: Union[str, None] = 'e841c8bb5871'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
