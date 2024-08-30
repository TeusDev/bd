"""treinador

Revision ID: 6bd8ba53e9ad
Revises: 9ec35cd38fc6
Create Date: 2024-08-30 13:41:41.646589

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '6bd8ba53e9ad'
down_revision = '9ec35cd38fc6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'treinador', ['telefone'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'treinador', type_='unique')
    # ### end Alembic commands ###
