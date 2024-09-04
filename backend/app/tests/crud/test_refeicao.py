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
from .utils import especialidades, random_datetime,start_date,end_date
# cpf and telefone
N = 11

def test_create_refeicao(db: Session) -> None:
    for i in range(50):
        data_avaliacao = random_datetime(start_date, end_date)
        peso         = round(random.uniform(40.0, 170.0),2)
        altura       = round(random.uniform(1.3,2.2),2)
        perc_gordura = round(random.uniform(4.0,30.0),2)
        id = random.randint(0,10000000)
        avaliacao = AvaliacaoCreate(
            id=id,
            data_avaliacao = data_avaliacao,
            peso = peso,
            altura = altura,
            perc_gordura = perc_gordura
        )
        
        existing_avaliacao = crud.get_avaliacoes(session=db,id=id)
        if existing_avaliacao:
            continue
        
        aval = crud.create_avaliacao(session=db,avaliacao_create=avaliacao)
        assert aval.data_avaliacao == data_avaliacao
        assert aval.peso == peso
        assert aval.altura == altura
        assert aval.perc_gordura == perc_gordura



def test_get_treinador(db: Session) -> None:
    for i in range(50):
        data_avaliacao = random_datetime(start_date, end_date)
        peso         = round(random.uniform(40.0, 170.0),2)
        altura       = round(random.uniform(1.3,2.2),2)
        perc_gordura = round(random.uniform(4.0,30.0),2)
        id = random.randint(0,10000000)
        avaliacao = AvaliacaoCreate(
           id=id,
           data_avaliacao = data_avaliacao,
           peso = peso,
           altura = altura,
           perc_gordura = perc_gordura)
        
        existing_avaliacao = crud.get_avaliacoes(session=db,id=id)
        if existing_avaliacao:
            continue
        
        aval = crud.create_avaliacao(session=db,avaliacao_create=avaliacao)
        
        existing_avaliacao2 = crud.get_avaliacoes(session=db,id=id)
        assert existing_avaliacao2

