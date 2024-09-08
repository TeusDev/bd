"""deleteall

Revision ID: d60013fd162b
Revises: e6e711282042
Create Date: 2024-09-08 03:43:59.217179

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'd60013fd162b'
down_revision = 'e6e711282042'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("DROP TABLE plano;")
    op.execute("DROP TABLE dieta_refeicoes;")
    op.execute("DROP TABLE dieta;")
    op.execute("DROP TABLE refeicao;")
    op.execute("DROP TABLE treino_sessao;")
    op.execute("DROP TABLE sessao;")
    op.execute("DROP TABLE treino_exercicio;")
    op.execute("DROP TABLE treino;")
    op.execute("DROP TABLE exercicio;")
    op.execute("DROP TABLE treinador_telefones;")
    op.execute("DROP TABLE treinador;")
    op.execute("DROP TABLE telefone;")


def downgrade():
    pass
