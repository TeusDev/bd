import uuid
from typing import Any,List,Dict


from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select,text
import re
from app import crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.models import (
    # Item,
    Message,
    UpdatePassword,
    User,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
<<<<<<< HEAD
    Telefone,
    TelefoneCreate,
    TelefonePublic,
=======
    Local,
>>>>>>> merge-jp-lucas-teusdev-thfer
    Treinador,
    TreinadorCreate,
    TreinadorPublic,
    TreinadoresPublic,
<<<<<<< HEAD
    TreinadorUpdate
)
from app.utils import generate_new_account_email, send_email
from .telefones import create_telefone
=======
    TreinadorUpdate,
    treinador_locais
)
from app.utils import generate_new_account_email, send_email
>>>>>>> merge-jp-lucas-teusdev-thfer
router = APIRouter()


@router.get(
    "/",
    response_model=TreinadoresPublic
)
def read_treinadores(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve treinadores.
    """

    count_statement = select(func.count()).select_from(Treinador)
    count = session.exec(count_statement).one()

    sql_query = text("""
    SELECT 
        treinador.id AS id_treinador,
        treinador.name AS name_treinador,
        treinador.especialidade AS espec_treinador,
<<<<<<< HEAD
        telefone_treinador.telefone as telefone_treinador
    FROM 
        treinador
    INNER JOIN 
        treinador_telefones ON treinador.id = treinador_telefones.treinador_id
    INNER JOIN 
        telefone as telefone_treinador ON treinador_telefones.telefone_id = telefone_treinador.telefone
=======
        treinador.telefone as telefone_treinador,
        local_de_treino.nome_local 
    FROM 
        treinador
    INNER JOIN 
        treinador_locais ON treinador.id = treinador_locais.treinador_id
    INNER JOIN 
        local as local_de_treino ON treinador_locais.local_id = local_de_treino.id
>>>>>>> merge-jp-lucas-teusdev-thfer
    LIMIT :limit OFFSET :skip
    """)
    
    results = session.execute(sql_query, {"limit": limit, "skip": skip}).all()

    treinadores = [
        TreinadorPublic(
            id=row[0],
            name=row[1],
            especialidade=row[2],
<<<<<<< HEAD
            telefone=row[3]
=======
            telefone=row[3],
            local_de_treino=row[4]
>>>>>>> merge-jp-lucas-teusdev-thfer
        )
        for row in results
    ]
    
    return TreinadoresPublic(data=treinadores, count=count)


@router.get(
    "/telefone",
    response_model=TreinadorPublic
)
<<<<<<< HEAD
def read_treinadores_tel(session: SessionDep, telefone:str) -> Any:
    """
    Retrieve treinadores by telefone.
    """

    statement = select(Treinador).where(Treinador.telefone == telefone)
=======
def read_treinadores_tel(session: SessionDep, id:str) -> Any:
    """
    Retrieve treinadores by id.
    """

    statement = select(Treinador).where(Treinador.id == id)
>>>>>>> merge-jp-lucas-teusdev-thfer
    treinador = session.exec(statement).all()

    return treinador


@router.get(
    "/especialidade",
    response_model=TreinadoresPublic
)
def read_treinadores_especialidade(session: SessionDep, especialidade:str,skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve treinadores by speciality.
    """

    count_statement = select(func.count()).select_from(Treinador).where(Treinador.especialidade == especialidade)
    count = session.exec(count_statement).one()

    statement = select(Treinador).where(Treinador.especialidade == especialidade).offset(skip).limit(limit)
    treinadores = session.exec(statement).all()

    return TreinadoresPublic(data=treinadores, count=count)


@router.post(
    "/",response_model=TreinadorPublic
)
<<<<<<< HEAD
def create_treinadores(*, session: SessionDep, treinador_in: TreinadorCreate,telefone:str) -> Any:
=======
def create_treinadores(*, session: SessionDep, treinador_in: TreinadorCreate,local_id:int) -> Any:
>>>>>>> merge-jp-lucas-teusdev-thfer
    """
    Create new treinador.
    """
    pattern = r"\d{8}"
<<<<<<< HEAD
    is_valid = bool(re.match(pattern,telefone))
=======
    is_valid = bool(re.match(pattern,treinador_in.telefone))
>>>>>>> merge-jp-lucas-teusdev-thfer
    if (not is_valid):
        raise HTTPException(
            status_code=400,
            detail="The telefone with this format is not valid.",
        )
<<<<<<< HEAD
        
    telefone_in = crud.get_telefones(session=session,telefone=telefone)
    if not telefone_in:
        raise HTTPException(
            status_code=400,
            detail="The telefone with this line doesnt exists in the system.",
        )
    treinador = crud.get_treinadores(session=session, telefone=telefone)
    if treinador:
        raise HTTPException(
            status_code=400,
            detail="The treinador with this line already exists in the system.",
        )

    treinador = crud.create_treinador(session=session, 
                                      treinador_create=treinador_in,
                                      telefone=telefone
                                      )
    
    sql_query = text("""
    SELECT 
        treinador.id,
        treinador.name ,
        treinador.especialidade,
        telefonez.telefone as telefones 
            
    FROM 
        treinador
    INNER JOIN 
        treinador_telefones ON treinador.id = treinador_telefones.treinador_id
    INNER JOIN 
        telefone AS telefonez ON treinador_telefones.telefone_id = telefonez.telefone
    WHERE 
        treinador.id = :treinador_id
=======
    statement = select(Treinador).where(Treinador.telefone == treinador_in.telefone)
    telefones = session.exec(statement).first()
    # telefone_in = crud.get_telefones(session=session,telefone=telefone)
    if telefones:
        raise HTTPException(
            status_code=400,
            detail="The telefone with this line already exists in the system.",
        )
    
    statement = select(Local).where(Local.id ==local_id)
    locais = session.exec(statement).first()
    # telefone_in = crud.get_telefones(session=session,telefone=telefone)
    if not locais:
        raise HTTPException(
            status_code=400,
            detail="The local with this id doesnt already exists in the system.",
        ) 
    
    
    treinador = crud.get_treinadores(session=session, id=treinador_in.id)
    if treinador:
        raise HTTPException(
            status_code=400,
            detail="The treinador with this id already exists in the system.",
        )

    treinador = crud.create_treinador(session=session, 
                                      treinador_create=treinador_in
                                      )
    
    local_ref = treinador_locais(
        treinador_id=treinador.id,
        local_id=local_id
    )
   
    # statement = select(treinador_telefones).where(treinador_telefones.treinador_id == treinador.id)
    statement=select(treinador_locais).where(treinador_locais.treinador_id==treinador.id
                                             and treinador_locais.local_id==local_id)
    warnings = session.exec(statement).first()
    if warnings:
        return Message(Message="relacao entre treinador e local ja existe")
    
    session.add(local_ref)
    session.commit()
    session.refresh(local_ref)
    
    
    sql_query = text("""
    SELECT 
        treinador.id AS id_treinador,
        treinador.name AS name_treinador,
        treinador.especialidade AS espec_treinador,
        treinador.telefone as telefone_treinador,
        local_de_treino.nome_local 
    FROM 
        treinador
    INNER JOIN 
        treinador_locais ON treinador.id = treinador_locais.treinador_id
    INNER JOIN 
        local as local_de_treino ON treinador_locais.local_id = local.id
>>>>>>> merge-jp-lucas-teusdev-thfer
    LIMIT :limit OFFSET :skip
    """)
    result = session.execute(
    sql_query,
    {"treinador_id": treinador_in.id, "limit": 1, "skip": 0}
)
    treinador = [
        TreinadorPublic(
            id=row[0],
            name=row[1],
            especialidade=row[2],
<<<<<<< HEAD
            telefone=row[3]
=======
            telefone=row[3],
            local_de_treino=row[4]
>>>>>>> merge-jp-lucas-teusdev-thfer
        )
        for row in result
    ]
    treinadorz = treinador[0]
    return treinadorz


<<<<<<< HEAD
@router.delete("/{telefone}")
def delete_treinadores(
    session: SessionDep, 
    telefone: str
=======
@router.delete("/{id}")
def delete_treinadores(
    session: SessionDep, 
    id: str
>>>>>>> merge-jp-lucas-teusdev-thfer
) -> Message:
    """
    Delete a treinador.
    """
<<<<<<< HEAD
    treinador = session.get(Treinador, telefone)
=======
    treinador = session.get(Treinador, id)
>>>>>>> merge-jp-lucas-teusdev-thfer
    if not treinador:
        raise HTTPException(status_code=404, detail="Treinador not found")
   
    session.delete(treinador)
    session.commit()
<<<<<<< HEAD
    return Message(message="Item deleted successfully")
=======
    return Message(message="Treinador deleted successfully")
>>>>>>> merge-jp-lucas-teusdev-thfer



@router.put(
    "/{telefone}", 
    response_model=TreinadorPublic
    )
def update_treinadores(
    *,
    session: SessionDep,
<<<<<<< HEAD
    treinador_in: TreinadorUpdate,
    telefone: str
=======
    treinador_in: TreinadorUpdate
>>>>>>> merge-jp-lucas-teusdev-thfer
) -> Any:
    """
    Update a treinador.
    """
<<<<<<< HEAD
    treinador = session.get(Treinador, telefone)
=======
    treinador = session.get(Treinador, treinador_in.id)
>>>>>>> merge-jp-lucas-teusdev-thfer
    if not treinador:
        raise HTTPException(status_code=404, detail="treinador not found")
   
    update_dict = treinador_in.model_dump(exclude_unset=True)
    treinador.sqlmodel_update(update_dict)
    session.add(treinador)
    session.commit()
    session.refresh(treinador)
    return treinador
