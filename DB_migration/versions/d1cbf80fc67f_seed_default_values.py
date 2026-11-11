"""seed default values

Revision ID: d1cbf80fc67f
Revises: 52bbd19f5a52
Create Date: 2026-11-05 19:44:35.815210

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1cbf80fc67f'
down_revision: Union[str, Sequence[str], None] = '52bbd19f5a52'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    status_table = sa.table("status", sa.column("status_name", sa.String))

    op.bulk_insert(status_table, [
        {"status_name": "Not Started"},
        {"status_name": "In Progress"},
        {"status_name": "Completed"},
    ])

    priority_table = sa.table("priorities", sa.column("priority_name", sa.String))

    op.bulk_insert(priority_table, [
        {"priority_name": "Low"},
        {"priority_name": "Medium"},
        {"priority_name": "High"},
    ])

    Role_table = sa.table("roles", sa.column("role_name", sa.String))
    
    op.bulk_insert(Role_table, [
        {"role_name": "Admin"},
        {"role_name": "Project Manager"},
        {"role_name": "Team Member"},
    ])

def downgrade() -> None:
    """Downgrade schema."""
    pass
