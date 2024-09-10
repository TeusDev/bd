import uuid
from typing import Any

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
    LocalBase,
    LocalCreate,
    LocalPublic,
    LocaisPublic
)
from app.utils import generate_new_account_email, send_email

router = APIRouter()


@router.get(
    "/",
    response_model=LocaisPublic
)
def read_locais(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve locais de treino.
    """

    count_statement = select(func.count()).select_from(Local)
    count = session.exec(count_statement).one()

    statement = select(Local).offset(skip).limit(limit)
    locais = session.exec(statement).all()

    return LocaisPublic(data=locais, count=count)


@router.post(
    "/",response_model=LocalPublic,  dependencies=[Depends(get_current_active_superuser)]
)
def create_local(*, session: SessionDep, local_in: LocalCreate) -> Any:
    """
    Create new local de treino.
    """
    
    statement = select(Local).where(Local.id == local_in.id)
    localz = session.exec(statement).first()
    
    # telefone = crud.get_telefones(session=session, telefone=telefone_in.telefone)
    if localz:
        raise HTTPException(
            status_code=400,
            detail="The Local with this ID already exists in the system.",
        )

    db_obj = Local.model_validate(
        local_in
    )
    
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


@router.put(
        "/{local_id}",
        response_model=Message,  dependencies=[Depends(get_current_active_superuser)]
)
def update_dieta(*, session: SessionDep, local_id: int, nome_novo:str) -> Any:
    """
    Update a dieta by ID.
    """
    # Fetch the existing dieta record
    stm = select(Local).where(Local.id==local_id)
    loc = session.exec(stm).first()
    if not loc:
        raise HTTPException(
            status_code=404,
            detail="Local not found.",
        )

    # Update dieta_refeicoes with new values
    sql_query = text("""
    UPDATE local
    SET 
        nome_local = :nome
    WHERE 
        local.id = :local_id;
    """)
    session.execute(
        sql_query,
        {
            "nome": nome_novo,
            "local_id": local_id
        }
    )
    session.commit()  # Commit the update

    return Message(message="Updated successfully")


@router.delete("/{local}",  dependencies=[Depends(get_current_active_superuser)])
def delete_local(
    session: SessionDep, local_id: int
) -> Message:
    """
    Delete a local.
    """
    local = session.get(Local, local_id)
    if not local:
        raise HTTPException(status_code=404, detail="local not found")
    session.delete(local)
    session.commit()
    return Message(message="Local deleted successfully")

