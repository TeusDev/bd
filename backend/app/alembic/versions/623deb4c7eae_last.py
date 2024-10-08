"""last

Revision ID: 623deb4c7eae
Revises: 745cb7fc61ba
Create Date: 2024-09-10 02:00:42.186433

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '623deb4c7eae'
down_revision = '745cb7fc61ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dieta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('exercicio',
    sa.Column('exercicio', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('grupo_muscular', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('local',
    sa.Column('nome_local', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('refeicao',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('calorias', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sessao',
    sa.Column('data', sa.DateTime(), nullable=False),
    sa.Column('duracao_minutos', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('treinador',
    sa.Column('telefone', sqlmodel.sql.sqltypes.AutoString(length=11), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.Column('especialidade', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(length=11), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('telefone')
    )
    op.create_table('treino',
    sa.Column('calorias', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('dieta_refeicoes',
    sa.Column('id_dieta', sa.Integer(), nullable=False),
    sa.Column('id_ref_manha', sa.Integer(), nullable=False),
    sa.Column('id_ref_tarde', sa.Integer(), nullable=False),
    sa.Column('id_ref_noite', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_dieta'], ['dieta.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_ref_manha'], ['refeicao.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_ref_noite'], ['refeicao.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_ref_tarde'], ['refeicao.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id_dieta', 'id_ref_manha', 'id_ref_tarde', 'id_ref_noite')
    )
    op.create_table('shape',
    sa.Column('nome_foto', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('foto', sa.LargeBinary(), nullable=True),
    sa.ForeignKeyConstraint(['usuario_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('treinador_locais',
    sa.Column('treinador_id', sqlmodel.sql.sqltypes.AutoString(length=11), nullable=False),
    sa.Column('local_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['local_id'], ['local.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['treinador_id'], ['treinador.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('treinador_id', 'local_id')
    )
    op.create_table('treino_exercicio',
    sa.Column('id_treino', sa.Integer(), nullable=False),
    sa.Column('id_exercicio', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_exercicio'], ['exercicio.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_treino'], ['treino.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id_treino', 'id_exercicio')
    )
    op.create_table('treino_sessao',
    sa.Column('id_treino1', sa.Integer(), nullable=False),
    sa.Column('id_treino2', sa.Integer(), nullable=False),
    sa.Column('id_treino3', sa.Integer(), nullable=False),
    sa.Column('id_sessao', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_sessao'], ['sessao.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_treino1'], ['treino.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_treino2'], ['treino.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_treino3'], ['treino.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id_treino1', 'id_treino2', 'id_treino3', 'id_sessao')
    )
    op.create_table('avaliacao',
    sa.Column('data_avaliacao', sa.DateTime(), nullable=False),
    sa.Column('peso', sa.Float(), nullable=False),
    sa.Column('altura', sa.Float(), nullable=False),
    sa.Column('perc_gordura', sa.Float(), nullable=False),
    sa.Column('shape_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['shape_id'], ['shape.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('plano',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('id_sessao_treino', sa.Integer(), nullable=True),
    sa.Column('id_treinador', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('id_avaliacao', sa.Integer(), nullable=True),
    sa.Column('id_dieta', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_avaliacao'], ['avaliacao.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_dieta'], ['dieta.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_sessao_treino'], ['sessao.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_treinador'], ['treinador.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'id_user')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('plano')
    op.drop_table('avaliacao')
    op.drop_table('treino_sessao')
    op.drop_table('treino_exercicio')
    op.drop_table('treinador_locais')
    op.drop_table('shape')
    op.drop_table('dieta_refeicoes')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('treino')
    op.drop_table('treinador')
    op.drop_table('sessao')
    op.drop_table('refeicao')
    op.drop_table('local')
    op.drop_table('exercicio')
    op.drop_table('dieta')
    # ### end Alembic commands ###
