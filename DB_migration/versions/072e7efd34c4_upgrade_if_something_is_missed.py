
"""upgrade if something is missed

Revision ID: 072e7efd34c4
Revises: 8db7b14d0f1a
Create Date: 2026-11-14 20:38:26.707688
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers
revision: str = '072e7efd34c4'
down_revision: Union[str, Sequence[str], None] = '8db7b14d0f1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # -------------------------------------------------
    # 1. Add missing columns to activity_log
    # -------------------------------------------------

    op.add_column(
        'activity_log',
        sa.Column('task_id', sa.Integer(), nullable=True)
    )

    op.add_column(
        'activity_log',
        sa.Column('field_name', sa.String(), nullable=True)
    )

    op.add_column(
        'activity_log',
        sa.Column('old_value', sa.String(), nullable=True)
    )

    op.add_column(
        'activity_log',
        sa.Column('new_value', sa.String(), nullable=True)
    )

    # Add foreign key for task_id
    op.create_foreign_key(
        'activity_log_task_id_fkey',
        'activity_log',
        'tasks',
        ['task_id'],
        ['task_id'],
        ondelete='CASCADE'
    )

    # -------------------------------------------------
    # 2. Remove old project status foreign key
    # -------------------------------------------------

    op.drop_constraint(
        'projects_status_fkey',
        'projects',
        type_='foreignkey'
    )

    # -------------------------------------------------
    # 3. Convert status names into status IDs
    # -------------------------------------------------

    op.alter_column(
        'projects',
        'status',
        existing_type=sa.VARCHAR(),
        type_=sa.Integer(),
        postgresql_using="""
            CASE status
                WHEN 'Not Started' THEN 1
                WHEN 'In Progress' THEN 2
                WHEN 'Completed' THEN 3
                ELSE NULL
            END
        """,
        existing_nullable=True
    )

    # -------------------------------------------------
    # 4. Create new foreign key referencing status_id
    # -------------------------------------------------

    op.create_foreign_key(
        'projects_status_fkey',
        'projects',
        'status',
        ['status'],
        ['status_id'],
        ondelete='SET NULL'
    )


def downgrade() -> None:

    # -------------------------------------------------
    # 1. Remove new project status foreign key
    # -------------------------------------------------

    op.drop_constraint(
        'projects_status_fkey',
        'projects',
        type_='foreignkey'
    )

    # -------------------------------------------------
    # 2. Convert status IDs back into status names
    # -------------------------------------------------

    op.alter_column(
        'projects',
        'status',
        existing_type=sa.Integer(),
        type_=sa.VARCHAR(),
        postgresql_using="""
            CASE status
                WHEN 1 THEN 'Not Started'
                WHEN 2 THEN 'In Progress'
                WHEN 3 THEN 'Completed'
                ELSE NULL
            END
        """,
        existing_nullable=True
    )

    # -------------------------------------------------
    # 3. Restore old foreign key referencing status_name
    # -------------------------------------------------

    op.create_foreign_key(
        'projects_status_fkey',
        'projects',
        'status',
        ['status'],
        ['status_name'],
        ondelete='SET NULL'
    )

    # -------------------------------------------------
    # 4. Remove activity_log foreign key
    # -------------------------------------------------

    op.drop_constraint(
        'activity_log_task_id_fkey',
        'activity_log',
        type_='foreignkey'
    )

    # -------------------------------------------------
    # 5. Remove newly added activity_log columns
    # -------------------------------------------------

    op.drop_column('activity_log', 'new_value')
    op.drop_column('activity_log', 'old_value')
    op.drop_column('activity_log', 'field_name')
    op.drop_column('activity_log', 'task_id')
