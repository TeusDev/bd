from fastapi.encoders import jsonable_encoder
from sqlmodel import Session
import uuid
from app import crud
from app.core.security import verify_password
from app.models import TreinadorCreate,Treinador,Telefone,TelefoneCreate
from app.tests.utils.utils import random_email, random_lower_string
import secrets
import string

# cpf and telefone
N = 11



def test_create_treinador(db: Session) -> None:
    telefone = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
              for i in range(N))
    treinador_id = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
              for i in range(N))
    telefone_in = TelefoneCreate(telefone=telefone)
    telefonek = crud.create_telefone(session=db, telefone_create=telefone_in)
    name = random_lower_string()
    especialidade = random_lower_string()
    treinador_in = TreinadorCreate(
        id=treinador_id,
        telefone = telefone,
        name = name,
        especialidade = especialidade
        )
    treinadork = crud.create_treinador(session=db, treinador_create=treinador_in)
    # assert treinadork.id == treinador_id
    assert treinadork.telefone == telefone
    assert treinadork.name == name
    assert treinadork.especialidade == especialidade



def test_get_treinador(db: Session) -> None:
   telefone = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
              for i in range(N))
   treinador_id = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
              for i in range(N))
   telefone_in = TelefoneCreate(telefone=telefone)
   telefonek = crud.create_telefone(session=db, telefone_create=telefone_in)
   name = random_lower_string()
   especialidade = random_lower_string()
   treinador_in = TreinadorCreate(
       id=treinador_id,
       telefone = telefone,
       name = name,
       especialidade = especialidade
       )
   treinadork = crud.create_treinador(session=db, treinador_create=treinador_in)
   existing_treinador = crud.get_treinadores(session=db,telefone=telefone)
   assert existing_treinador

