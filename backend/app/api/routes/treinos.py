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
    Treino,
    TreinoCreate,
    TreinoPublic,
    TreinosPublic,
    Message
)
from app.utils import generate_new_account_email, send_email

router = APIRouter()


@router.get(
    "/",
    response_model=TreinosPublic
)
def read_treinos(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve treinos.
    """

    count_statement = select(func.count()).select_from(Treino)
    count = session.exec(count_statement).one()

    statement = select(Treino).offset(skip).limit(limit)
    treinos = session.exec(statement).all()

    return TreinosPublic(data=treinos, count=count)


@router.post(
    "/",response_model=TreinoPublic
)
def create_treino(*, session: SessionDep, treino_in: TreinoCreate) -> Any:
    """
    Create new treino.
    """
    exercicio = crud.get_exercicios(session=session, id=treino_in.id_exercicio)
    if not exercicio:
        raise HTTPException(
            status_code=400,
            detail="The exercicio with this id doesnt exists in the system.",
        )
        
    treino = crud.get_treinos(session=session, id=treino_in.id)
    if treino:
        raise HTTPException(
            status_code=400,
            detail="The treino with this id already exists in the system.",
        )
        
        
    treino = crud.create_treino(session=session, treino_create=treino_in)
    return treino

@router.delete("/{treino}")
def delete_treino(
    session: SessionDep, id: str
) -> Message:
    """
    Delete a treino.
    """
    treino = session.get(Treino, id)
    if not treino:
        raise HTTPException(status_code=404, detail="treino not found")
    session.delete(treino)
    session.commit()
    return Message(message="Treino deleted successfully")

