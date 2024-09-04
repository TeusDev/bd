"""new

Revision ID: b9b1cb9e66ab
Revises: 21a08fd4db03
Create Date: 2024-08-30 20:16:02.190029

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'b9b1cb9e66ab'
down_revision = '21a08fd4db03'
branch_labels = None
depends_on = None

def upgrade():
    # Delete all records from the tables
    op.execute("DELETE FROM telefone;")

def downgrade():
    # Delete all records from the tables
    op.execute("DELETE FROM telefone;")
    
