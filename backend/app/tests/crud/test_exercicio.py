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
    ExerciciosPublic
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

def test_create_exercicio(db: Session) -> None:
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

