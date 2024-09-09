from fastapi.encoders import jsonable_encoder
from sqlmodel import Session
import uuid
from app import crud
from app.core.security import verify_password
from app.models import (
    Refeicao,
    RefeicaoCreate,
    RefeicaoPublic,
    RefeicoesPublic
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
    diet_meals
)
    
# cpf and telefone
N=8

def test_create_refeicao(db: Session) -> None:
    for i in range(40):
        nome_dieta = random.choice(diet_meals)
        calorias = random.randint(300,2000)
        id = random.randint(0,10000000)
        refeicao = RefeicaoCreate(
            id=id,
            name=nome_dieta,
            calorias=calorias
        )
        
        existing_ref = crud.get_refeicao(session=db,refeicao_id=id)
        if existing_ref:
            continue
        
        refeicoes = crud.create_refeicao(session=db,refeicao_create=refeicao)
        assert refeicao.id == id
        assert refeicao.name == nome_dieta
        assert refeicao.calorias == calorias
