"""new

Revision ID: 9eb9ca05c7ee
Revises: 7961c6522bdf
Create Date: 2024-09-10 00:35:39.879018

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '1a31ce608336'
down_revision = '7961c6522bdf'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("DROP TABLE plano;")
    op.execute("DROP TABLE dieta_refeicoes;")
    op.execute("DROP TABLE dieta;")
    op.execute("DROP TABLE refeicao;")
    op.execute("DROP TABLE avaliacao;")
    op.execute("DROP TABLE shape;")
    op.execute("DROP TABLE treinador_locais;")
    op.execute("DROP TABLE treinador;")
    op.execute("DROP TABLE local;")
    op.execute("DROP TABLE treino_sessao;")
    op.execute("DROP TABLE treino_exercicio;")
    op.execute("DROP TABLE sessao;")
    op.execute("DROP TABLE treino;")
    op.execute("DROP VIEW exercicios_com_pernas")
    op.execute("DROP VIEW exercicios_cardio")
    op.execute("DROP TABLE exercicio;")
    op.execute('DROP TABLE "user";')

def downgrade():
    pass
