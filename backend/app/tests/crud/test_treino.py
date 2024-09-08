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
N=8

def test_create_treino(db: Session) -> None:
    for i in range(25):
        exercicio_aleatorio = random.choice(list(exerciciosh.keys()))
        id = random.randint(0,10000000)
        exercicioa = Exercicio(
            id=id,
            exercicio=exercicio_aleatorio,
            grupo_muscular=exerciciosh[exercicio_aleatorio]
        )
        stm01 = select(Exercicio).where(Exercicio.id==id)
        existing_ex = db.exec(stm01).first()
        if existing_ex:
            continue
        
        db.add(exercicioa)
        db.commit()
        db.refresh(exercicioa)
        
        
        calorias = random.randint(300,2000)

        treino = Treino(
            id=id,
            calorias=calorias
        )
        
        stm02 = select(Treino).where(Treino.id==id)
        existing_treino = db.exec(stm02).first()
        if existing_treino:
            continue
            
        db.add(treino)
        db.commit()
        db.refresh(treino)
         
           
        treino_exercicios = treino_exercicio(
            id_treino=treino.id,
            id_exercicio=exercicioa.id
        )
        
        stm1 = select(treino_exercicio).where(treino_exercicio.id_treino==treino.id)
        tr = db.exec(stm1).first()
        if tr:
            continue
        
        db.add(treino_exercicios)
        db.commit()
        db.refresh(treino_exercicios)
        
        
        

