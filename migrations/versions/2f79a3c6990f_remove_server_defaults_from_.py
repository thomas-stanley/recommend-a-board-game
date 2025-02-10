"""Remove server_defaults from bayesaverage and is_expansion

Revision ID: 2f79a3c6990f
Revises: de1ce90f91dc
Create Date: 2025-02-10 19:54:50.087190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f79a3c6990f'
down_revision = 'de1ce90f91dc'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("board_game") as batch_op:
        batch_op.alter_column("bayesaverage", existing_type=sa.Float, server_default=None)
        batch_op.alter_column("is_expansion", existing_type=sa.Boolean, server_default=None)


def downgrade():
    with op.batch_alter_table("board_game") as batch_op:
        batch_op.alter_column("bayesaverage", existing_type=sa.Float, server_default="0.0")
        batch_op.alter_column("is_expansion", existing_type=sa.Boolean, server_default="0")
