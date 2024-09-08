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
    Dieta,
    DietaCreate,
    DietaPublic,
    DietasPublic,
    dieta_refeicoes
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
N = 11

def test_create_dieta(db: Session) -> None:
    for i in range(20):
        nome_dieta1 = random.choice(diet_meals)
        nome_dieta2 = random.choice(diet_meals)
        nome_dieta3 = random.choice(diet_meals)
        
        calorias1 = random.randint(300,2000)
        calorias2 = random.randint(300,2000)
        calorias3 = random.randint(300,2000)

        id1 = random.randint(0,10000000)
        id2 = random.randint(0,10000000)
        id3 = random.randint(0,10000000)

        refeicao1 = RefeicaoCreate(
            id=id1,
            name=nome_dieta1,
            calorias=calorias1
        )
        
        refeicao2 = RefeicaoCreate(
            id=id2,
            name=nome_dieta2,
            calorias=calorias3
        )
        refeicao3 = RefeicaoCreate(
            id=id3,
            name=nome_dieta3,
            calorias=calorias3
        )
        
        existing_ref1 = crud.get_refeicao(session=db,id=id1)
        existing_ref2 = crud.get_refeicao(session=db,id=id2)
        existing_ref3 = crud.get_refeicao(session=db,id=id3)

        if existing_ref1 or existing_ref2 or existing_ref3:
            continue
        
        refeicoes1 = crud.create_refeicao(session=db,refeicao_create=refeicao1)
        refeicoes2 = crud.create_refeicao(session=db,refeicao_create=refeicao2)
        refeicoes3 = crud.create_refeicao(session=db,refeicao_create=refeicao3)

        
        
        id = random.randint(0,10000000)
        
          
        existing_ref = crud.get_refeicao(session=db,id=id)
        if existing_ref:
            continue
        
        name = f"dieta_{id}"
        dieta = DietaCreate(
            id=id,
            name=name
        )
        
        existing_dieta = crud.get_dieta(session=db,id=id)
        if existing_dieta:
            continue
        
        dietas = crud.create_dieta(session=db,dieta_create=dieta)
        assert dietas.id == id
        assert dietas.id_ref_manha == id1
        assert dietas.id_ref_tarde == id2
        assert dietas.id_ref_noite == id3
        
        dieta_refeicoez = dieta_refeicoes(
            id_dieta=dieta.id,
            id_ref_manha=refeicao1.id,
            id_ref_tarde=refeicao2.id,
            id_ref_noite=refeicao3.id
        )
        
        db.add(dieta_refeicoez)
        db.commit()
        db.refresh(dieta_refeicoez)
        
        
