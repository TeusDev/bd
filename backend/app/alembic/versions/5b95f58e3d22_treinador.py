"""treinador

Revision ID: 5b95f58e3d22
Revises: 6bd8ba53e9ad
Create Date: 2024-08-30 13:56:29.869968

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '5b95f58e3d22'
down_revision = '6bd8ba53e9ad'
branch_labels = None
depends_on = None


def upgrade():
    # Delete all records from the tables
    op.execute("DROP TABLE TREINADOR;")
    
    op.execute("DELETE FROM telefone;")
    # Change the length of the column
    op.alter_column('telefone', 'telefone',
                    type_=sa.String(length=20),  # Adjust length as needed
                    existing_type=sa.String(length=11))

def downgrade():
    # Delete all records from the tables
    op.execute("DELETE FROM telefone;")
    
    # Revert the column length if needed
    op.alter_column('telefone', 'telefone',
                    type_=sa.String(length=11),
                    existing_type=sa.String(length=20))
