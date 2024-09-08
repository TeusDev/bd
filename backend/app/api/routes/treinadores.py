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
    Telefone,
    TelefoneCreate,
    TelefonePublic,
    Treinador,
    TreinadorCreate,
    TreinadorPublic,
    TreinadoresPublic,
    treinador_telefones,
    TreinadorUpdate
)
from app.utils import generate_new_account_email, send_email
from .telefones import create_telefone
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
        telefone_treinador.telefone as telefone_treinador
    FROM 
        treinador
    INNER JOIN 
        treinador_telefones ON treinador.id = treinador_telefones.treinador_id
    INNER JOIN 
        telefone as telefone_treinador ON treinador_telefones.telefone_id = telefone_treinador.telefone
    LIMIT :limit OFFSET :skip
    """)
    
    results = session.execute(sql_query, {"limit": limit, "skip": skip}).all()

    treinadores = [
        TreinadorPublic(
            id=row[0],
            name=row[1],
            especialidade=row[2],
            telefone=row[3]
        )
        for row in results
    ]
    
    return TreinadoresPublic(data=treinadores, count=count)


@router.get(
    "/telefone",
    response_model=TreinadorPublic
)
def read_treinadores_tel(session: SessionDep, telefone:str) -> Any:
    """
    Retrieve treinadores by telefone.
    """

    statement = select(Treinador).where(Treinador.telefone == telefone)
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
def create_treinadores(*, session: SessionDep, treinador_in: TreinadorCreate,telefone:str) -> Any:
    """
    Create new treinador.
    """
    pattern = r"\d{8}"
    is_valid = bool(re.match(pattern,telefone))
    if (not is_valid):
        raise HTTPException(
            status_code=400,
            detail="The telefone with this format is not valid.",
        )
        
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
    
     
    telefone_ref = treinador_telefones(
        treinador_id=treinador.id,
        telefone_id=telefone
    )
    
    statement = select(treinador_telefones).where(treinador_telefones.treinador_id == treinador.id)
    warnings = session.exec(statement).first()
    if warnings:
        return Message(Message="relacao entre treinador e telefone ja existe")
    
    session.add(telefone_ref)
    session.commit()
    session.refresh(telefone_ref)
    
    
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
            telefone=row[3]
        )
        for row in result
    ]
    treinadorz = treinador[0]
    return treinadorz


@router.delete("/{telefone}")
def delete_treinadores(
    session: SessionDep, 
    telefone: str
) -> Message:
    """
    Delete a treinador.
    """
    treinador = session.get(Treinador, telefone)
    if not treinador:
        raise HTTPException(status_code=404, detail="Treinador not found")
   
    session.delete(treinador)
    session.commit()
    return Message(message="Item deleted successfully")



@router.put(
    "/{telefone}", 
    response_model=TreinadorPublic
    )
def update_treinadores(
    *,
    session: SessionDep,
    treinador_in: TreinadorUpdate,
    telefone: str
) -> Any:
    """
    Update a treinador.
    """
    treinador = session.get(Treinador, telefone)
    if not treinador:
        raise HTTPException(status_code=404, detail="treinador not found")
   
    update_dict = treinador_in.model_dump(exclude_unset=True)
    treinador.sqlmodel_update(update_dict)
    session.add(treinador)
    session.commit()
    session.refresh(treinador)
    return treinador
