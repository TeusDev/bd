from fastapi.encoders import jsonable_encoder
from sqlmodel import Session,select
import uuid
from app import crud
from app.core.security import verify_password
<<<<<<< HEAD
from app.models import TreinadorCreate,Treinador,Telefone,TelefoneCreate,treinador_telefones
=======
from app.models import TreinadorCreate,Treinador,Local,LocalCreate,treinador_locais
>>>>>>> merge-jp-lucas-teusdev-thfer
from app.tests.utils.utils import random_email, random_lower_string
import secrets
import string
from .nome_gen import choose_name
import random
<<<<<<< HEAD
from .utils import especialidades
=======
from .utils import especialidades,academias
>>>>>>> merge-jp-lucas-teusdev-thfer
# cpf and telefone
N=8



def test_create_treinador(db: Session) -> None:
<<<<<<< HEAD
    for i in range(20):
        telefone = ''.join(secrets.choice(string.digits) for i in range(N))
        treinador_id = ''.join(secrets.choice(string.digits) for i in range(N))
        telefone_in = TelefoneCreate(telefone=telefone)
        existing_telefone = crud.get_telefones(session=db, telefone=telefone)
        if existing_telefone:
            continue
        telefonek = crud.create_telefone(session=db, telefone_create=telefone_in)
=======
    for i in range(40):
        ################### creating local ############################
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
        ##################################################################
        
        telefone = ''.join(secrets.choice(string.digits) for i in range(N))
        treinador_id = ''.join(secrets.choice(string.digits) for i in range(N))
        
        
        
>>>>>>> merge-jp-lucas-teusdev-thfer
        name = choose_name()
        especialidade = random.choice(especialidades)
        treinador_in = TreinadorCreate(
            id=treinador_id,
            telefone = telefone,
            name = name,
            especialidade = especialidade
            )
<<<<<<< HEAD
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
=======
        statement = select(Treinador).where(Treinador.telefone == treinador_in.telefone)
        existing_telefone = db.exec(statement).first()
        
        if existing_telefone:
            continue
        existing_treinador = crud.get_treinadores(session=db,id=treinador_id)
        if existing_treinador:
            continue
        treinadork = crud.create_treinador(session=db, treinador_create=treinador_in)
        
        treinador_locaiz = treinador_locais(
            treinador_id=treinadork.id,
            local_id=local_in.id
        )
        statement = select(treinador_locais).where(treinador_locais.treinador_id == treinador_id
                                                   and treinador_locais.local_id==treinador_locaiz.local_id)
        warnings = db.exec(statement).first()
        if warnings:
            continue
        db.add(treinador_locaiz)
        db.commit()
        db.refresh(treinador_locaiz)
>>>>>>> merge-jp-lucas-teusdev-thfer
        


