"""drop all tables

Revision ID: 21a08fd4db03
Revises: 5b95f58e3d22
Create Date: 2024-08-30 14:04:34.536455

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '21a08fd4db03'
down_revision = '5b95f58e3d22'
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
