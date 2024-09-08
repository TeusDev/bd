from fastapi.encoders import jsonable_encoder
from sqlmodel import Session
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
    TreinoCreate
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
N = 11

def test_create_treino(db: Session) -> None:
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
        assert exerciciosz.name ==exercicio_aleatorio
        assert exerciciosz.calorias == exerciciosh[exercicio_aleatorio]
        
        calorias = random.randint(300,2000)

        treino = TreinoCreate(
            id=id,
            calorias=calorias
        )
        
        existing_treino = crud.get_treinos(session=db,id=id)
        if existing_treino:
            continue
        
        treinosz = crud.create_treino(session=db,treino_create=treino)
        assert treinosz.id == id
        assert treinosz.calorias == calorias
        
        treino_exercicio = treino_exercicio(
            id_treino=treinosz.id,
            id_exercicio=treinosz.id_exercicio
        )
        
        db.add(treino_exercicio)
        db.commit()
        db.refresh(treino_exercicio)
        
        
        

