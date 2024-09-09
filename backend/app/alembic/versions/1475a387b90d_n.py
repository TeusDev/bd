"""n

Revision ID: 1475a387b90d
Revises: 
Create Date: 2024-09-09 09:58:40.318814

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '77dceb3948e3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("DROP TABLE plano;")
    op.execute("DROP TABLE dieta_refeicoes;")
    op.execute("DROP TABLE dieta;")
    op.execute("DROP TABLE refeicao;")
    op.execute("DROP TABLE avaliacao;")
    op.execute("DROP TABLE shape;")
    op.execute("DROP TABLE treinador_telefones;")
    op.execute("DROP TABLE treinador;")
    op.execute("DROP TABLE telefone;")
    op.execute("DROP TABLE treino_sessao;")
    op.execute("DROP TABLE treino_exercicio;")
    op.execute("DROP TABLE sessao;")
    op.execute("DROP TABLE treino;")
    op.execute("DROP TABLE exercicio;")


def downgrade():
    pass
