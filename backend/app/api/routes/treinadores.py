import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select

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
    TelefoneRegister,
    TelefonePublic,
    Treinador,
    TreinadorCreate,
    TreinadorRegister,
    TreinadorPublic,
    TreinadoresPublic,
    TreinadorUpdate
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

    statement = select(Treinador).offset(skip).limit(limit)
    treinadores = session.exec(statement).all()

    return TreinadoresPublic(data=treinadores, count=count)


@router.post(
    "/",response_model=TreinadorPublic
)
def create_treinadores(*, session: SessionDep, treinador_in: TreinadorCreate) -> Any:
    """
    Create new treinador.
    """
    treinador = crud.get_treinadores(session=session, telefone=treinador_in.telefone)
    if treinador:
        raise HTTPException(
            status_code=400,
            detail="The treinador with this line already exists in the system.",
        )

    treinador = crud.create_treinador(session=session, treinador_create=treinador_in)
    return treinador


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
