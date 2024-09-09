# from fastapi.encoders import jsonable_encoder
# from sqlmodel import Session

# from app import crud
# from app.core.security import verify_password
# from app.models import User, UserCreate, UserUpdate,Telefone,TelefoneCreate
# from app.tests.utils.utils import random_email, random_lower_string
# import secrets
# import string

# # cpf and telefone
# N = 8


# def test_create_telefone(db: Session) -> None:
#     for i in range(40):
#         telefonez = ''.join(secrets.choice(string.digits) for i in range(N))
#         telefone_in = TelefoneCreate(telefone=telefonez)
#         existing_telefone = crud.get_telefones(session=db, telefone=telefonez)
#         if existing_telefone:
#             continue
#         telefonek = crud.create_telefone(session=db, telefone_create=telefone_in)
#         assert telefonek.telefone == telefonez

