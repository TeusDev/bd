"""N

Revision ID: 339a96870d8c
Revises: 
Create Date: 2024-09-09 19:57:27.766427

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '6c0d94c0e9a5'
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
