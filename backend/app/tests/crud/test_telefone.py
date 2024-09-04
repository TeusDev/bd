from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from app import crud
from app.core.security import verify_password
from app.models import User, UserCreate, UserUpdate,Telefone,TelefoneCreate
from app.tests.utils.utils import random_email, random_lower_string
import secrets
import string

# cpf and telefone
N = 11


def test_create_telefone(db: Session) -> None:
    for i in range(50):
        telefonez = ''.join(secrets.choice(string.digits) for i in range(N))
        telefone_in = TelefoneCreate(telefone=telefonez)
        existing_telefone = crud.get_telefones(session=db, telefone=telefonez)
        if existing_telefone:
            continue
        telefonek = crud.create_telefone(session=db, telefone_create=telefone_in)
        assert telefonek.telefone == telefonez


def test_get_telefone(
    db: Session
) -> None:
    for i in range(50):
        telefone = ''.join(secrets.choice(string.digits) for i in range(N))
        telefone_in = TelefoneCreate(telefone=telefone)
        existing_telefone = crud.get_telefones(session=db, telefone=telefone)
        if existing_telefone:
            continue
        telefone2 = crud.create_telefone(session=db, telefone_create=telefone_in)
        existing_telefone = crud.get_telefones(session=db, telefone=telefone)
        assert existing_telefone

