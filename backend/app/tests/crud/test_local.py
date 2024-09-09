from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from app import crud
from app.core.security import verify_password
from app.models import Local,LocaisPublic,LocalCreate,LocalPublic
from app.tests.utils.utils import random_email, random_lower_string
from .utils import academias
import random
import secrets
import string

# cpf and telefone
N = 8


def test_create_local(db: Session) -> None:
    for i in range(20):
        local = random.choice(academias)
        id1 = random.randint(0,10000000)
        local_in = TelefoneCreate(telefone=telefonez)
        existing_telefone = crud.get_telefones(session=db, telefone=telefonez)
        if existing_telefone:
            continue
        telefonek = crud.create_telefone(session=db, telefone_create=telefone_in)
        assert telefonek.telefone == telefonez

