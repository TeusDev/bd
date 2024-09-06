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
    Exercicio,
    ExercicioBase,
    ExercicioCreate,
    ExercicioPublic,
    ExerciciosPublic,
    Message
)
from app.utils import generate_new_account_email, send_email

router = APIRouter()


@router.get(
    "/",
    response_model=ExerciciosPublic
)
def read_exercicios(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve exercicios.
    """

    count_statement = select(func.count()).select_from(Exercicio)
    count = session.exec(count_statement).one()

    statement = select(Exercicio).offset(skip).limit(limit)
    exercicios = session.exec(statement).all()

    return ExerciciosPublic(data=exercicios, count=count)


@router.post(
    "/",response_model=ExercicioPublic
)
def create_exercicio(*, session: SessionDep, exercicio_in: ExercicioCreate) -> Any:
    """
    Create new exercicio.
    """
    exercicio = crud.get_exercicios(session=session, id=exercicio_in.id)
    if exercicio:
        raise HTTPException(
            status_code=400,
            detail="The exercicio with this id already exists in the system.",
        )
        
    exercicio = crud.create_exercicio(session=session, exercicio_create=exercicio_in)
    return exercicio

@router.delete("/{exercicio}")
def delete_exercicio(
    session: SessionDep, id: str
) -> Message:
    """
    Delete a exercicio.
    """
    exercicio = session.get(Exercicio, id)
    if not exercicio:
        raise HTTPException(status_code=404, detail="exercicio not found")
    session.delete(exercicio)
    session.commit()
    return Message(message="Exercicio deleted successfully")

