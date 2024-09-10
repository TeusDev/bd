from fastapi.encoders import jsonable_encoder
from sqlmodel import Session,select

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
    for i in range(10):
        local = random.choice(academias)
        id1 = random.randint(0,10000000)
        local_in = LocalCreate(id=id1,nome_local=local)
        statement = select(Local).where(Local.id == id1)
        existing_locais = db.exec(statement).first()
        if existing_locais:
            continue
        db_obj = Local.model_validate(local_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        assert db_obj.id == id1

