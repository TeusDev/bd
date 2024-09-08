from fastapi.encoders import jsonable_encoder
from sqlmodel import Session,select
import uuid
from app import crud
from app.core.security import verify_password
from app.models import TreinadorCreate,Treinador,Telefone,TelefoneCreate,treinador_telefones
from app.tests.utils.utils import random_email, random_lower_string
import secrets
import string
from .nome_gen import choose_name
import random
from .utils import especialidades
# cpf and telefone
N = 11



def test_create_treinador(db: Session) -> None:
    for i in range(20):
        telefone = ''.join(secrets.choice(string.digits) for i in range(N))
        treinador_id = ''.join(secrets.choice(string.digits) for i in range(N))
        telefone_in = TelefoneCreate(telefone=telefone)
        existing_telefone = crud.get_telefones(session=db, telefone=telefone)
        if existing_telefone:
            continue
        telefonek = crud.create_telefone(session=db, telefone_create=telefone_in)
        name = choose_name()
        especialidade = random.choice(especialidades)
        treinador_in = TreinadorCreate(
            id=treinador_id,
            telefone = telefone,
            name = name,
            especialidade = especialidade
            )
        existing_treinador = crud.get_treinadores(session=db,telefone=telefone)
        if existing_treinador:
            continue
        treinadork = crud.create_treinador(session=db, treinador_create=treinador_in,telefone=telefone)
        # assert treinadork.id == treinador_id
        # assert treinadork.telefone == telefone
        # assert treinadork.name == name
        # assert treinadork.especialidade == especialidade
        
        treinador_telefonesz = treinador_telefones(
            treinador_id=treinadork.id,
            telefone_id=telefone_in.telefone
        )
        statement = select(treinador_telefones).where(treinador_telefones.treinador_id == treinador_id)
        warnings = db.exec(statement).first()
        if warnings:
            continue
        db.add(treinador_telefonesz)
        db.commit()
        db.refresh(treinador_telefonesz)
        


