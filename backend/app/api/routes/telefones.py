import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select
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
    TelefonesPublic
)
from app.utils import generate_new_account_email, send_email

router = APIRouter()


@router.get(
    "/",
    response_model=TelefonesPublic
)
def read_telefones(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve telefones.
    """

    count_statement = select(func.count()).select_from(Telefone)
    count = session.exec(count_statement).one()

    statement = select(Telefone).offset(skip).limit(limit)
    telefones = session.exec(statement).all()

    return TelefonesPublic(data=telefones, count=count)


@router.post(
    "/",response_model=TelefonePublic
)
def create_telefone(*, session: SessionDep, telefone_in: TelefoneCreate) -> Any:
    """
    Create new telefone.
    """
    telefone = crud.get_telefones(session=session, telefone=telefone_in.telefone)
    if telefone:
        raise HTTPException(
            status_code=400,
            detail="The telefone with this line already exists in the system.",
        )

    pattern = r"\d{8}"
    is_valid = bool(re.match(pattern,telefone_in.telefone))
    if (not is_valid):
        raise HTTPException(
            status_code=400,
            detail="The telefone with this format is not valid.",
        )
    telefone = crud.create_telefone(session=session, telefone_create=telefone_in)
    return telefone

@router.delete("/{telefone}")
def delete_telefone(
    session: SessionDep, telefone: str
) -> Message:
    """
    Delete a telefone.
    """
    telefone = session.get(Telefone, telefone)
    if not telefone:
        raise HTTPException(status_code=404, detail="telefone not found")
    session.delete(telefone)
    session.commit()
    return Message(message="Item deleted successfully")

