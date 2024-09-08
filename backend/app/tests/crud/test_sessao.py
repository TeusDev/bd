from fastapi.encoders import jsonable_encoder
from sqlmodel import Session,select
import uuid
from app import crud
from app.core.security import verify_password
from app.models import (
    Refeicao,
    RefeicaoCreate,
    RefeicaoPublic,
    RefeicoesPublic,
    Exercicio,
    ExercicioCreate,
    ExercicioPublic,
    ExerciciosPublic,
    treino_exercicio,
    Treino,
    TreinoPublic,
    TreinoCreate,
    Sessao,
    SessaoCreate,
    treino_sessao
)
from app.tests.utils.utils import random_email, random_lower_string
import secrets
import string
from .nome_gen import choose_name
import random
from .utils import (
    especialidades, 
    random_datetime,
    start_date,
    end_date,
    exerciciosh,
    diet_meals
)
    
# cpf and telefone
N=8

def test_create_sessao(db: Session) -> None:
    for i in range(25):
        exercicio_aleatorio = random.choice(list(exerciciosh.keys()))
        id = random.randint(0,10000000)
        exercicio = ExercicioCreate(
            id=id,
            exercicio=exercicio_aleatorio,
            grupo_muscular=exerciciosh[exercicio_aleatorio]
        )
        
        existing_ex = crud.get_exercicios(session=db,id=id)
        if existing_ex:
            continue
        
        exerciciosz = crud.create_exercicio(session=db,exercicio_create=exercicio)
        assert exerciciosz.id == id
        
        calorias = random.randint(300,2000)

        treino = TreinoCreate(
            id=id,
            calorias=calorias
        )
        
        existing_treino = crud.get_treinos(session=db,id=id)
        if existing_treino:
            continue
        
        treinosz = crud.create_treino(session=db,treino_create=treino,exercicio=exercicio.id)
        assert treinosz.id == id
        assert treinosz.calorias == calorias
        
        treino_exercicioz = treino_exercicio(
            id_treino=treinosz.id,
            id_exercicio=exerciciosz.id
        )
        
        statement = select(treino_exercicio).where(treino_exercicio.id_treino == treinosz.id)
        warnings = db.exec(statement).first()
        if warnings:
            continue
        
        db.add(treino_exercicioz)
        db.commit()
        db.refresh(treino_exercicioz)
        
        duracao_minutos = random.randint(15,120)
        data_avaliacao = random_datetime(start_date, end_date)

        existing_session = crud.get_sessoes(session=db,id=id)
        if existing_session:
            continue
        sessaoz = Sessao (
            id =id,
            data=data_avaliacao,
            duracao_minutos=duracao_minutos
        )
        session = crud.create_sessao(session=db,sessao_create=sessaoz,treino_ids=[treino.id,treino.id,treino.id])
        
        treino_session = treino_sessao (
            id_treino1 = id,
            id_treino2 = id,
            id_treino3 = id,
            id_sessao=id
        )        
        
        statement = select(treino_session).where(treino_session.id_sessao == sessaoz.id)
        warnings = db.exec(statement).first()
        if warnings:
            continue
        
        db.add(treino_sessao)
        db.commit()
        db.refresh(treino_sessao)
        
        assert sessaoz.id == id
        
        
        

