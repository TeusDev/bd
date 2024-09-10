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
    Local,
    Treinador,
    TreinadorCreate,
    TreinadorPublic,
    TreinadoresPublic,
    TreinadorUpdate,
    treinador_locais
)
from app.utils import generate_new_account_email, send_email
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
        treinador.telefone as telefone_treinador,
        local_de_treino.nome_local 
    FROM 
        treinador
    INNER JOIN 
        treinador_locais ON treinador.id = treinador_locais.treinador_id
    INNER JOIN 
        local as local_de_treino ON treinador_locais.local_id = local_de_treino.id
    LIMIT :limit OFFSET :skip
    """)
    
    results = session.execute(sql_query, {"limit": limit, "skip": skip}).all()

    treinadores = [
        TreinadorPublic(
            id=row[0],
            name=row[1],
            especialidade=row[2],
            telefone=row[3],
            local_de_treino=row[4]
        )
        for row in results
    ]
    
    return TreinadoresPublic(data=treinadores, count=count)


@router.get(
    "/id",
    response_model=TreinadorPublic
)
def read_treinadores_id(session: SessionDep, id:str) -> Any:
    """
    Retrieve treinadores by id.
    """

    statement = select(Treinador).where(Treinador.id == id)
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
    "/",response_model=TreinadorPublic,    dependencies=[Depends(get_current_active_superuser)]
)
def create_treinadores(*, session: SessionDep, treinador_in: TreinadorCreate,local_id:int) -> Any:
    """
    Create new treinador.
    """
    pattern = r"\d{8}"
    is_valid = bool(re.match(pattern,treinador_in.telefone))
    if (not is_valid):
        raise HTTPException(
            status_code=400,
            detail="The telefone with this format is not valid.",
        )
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
            telefone=row[3],
            local_de_treino=row[4]
        )
        for row in result
    ]
    treinadorz = treinador[0]
    return treinadorz


@router.delete("/{id}",    dependencies=[Depends(get_current_active_superuser)])
def delete_treinadores(
    session: SessionDep, 
    id: str
) -> Message:
    """
    Delete a treinador.
    """
    treinador = session.get(Treinador, id)
    if not treinador:
        raise HTTPException(status_code=404, detail="Treinador not found")
   
    session.delete(treinador)
    session.commit()
    return Message(message="Treinador deleted successfully")



@router.put(
    "/{id}", 
    response_model=TreinadorPublic,    dependencies=[Depends(get_current_active_superuser)]
    )
def update_treinadores(
    *,
    session: SessionDep,
    treinador_in: TreinadorUpdate
) -> Any:
    """
    Update a treinador.
    """
    treinador = session.get(Treinador, treinador_in.id)
    if not treinador:
        raise HTTPException(status_code=404, detail="treinador not found")
   
    update_dict = treinador_in.model_dump(exclude_unset=True)
    treinador.sqlmodel_update(update_dict)
    session.add(treinador)
    session.commit()
    session.refresh(treinador)
    return treinador
