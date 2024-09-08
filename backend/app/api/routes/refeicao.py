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
    Refeicao,
    RefeicaoCreate,
    RefeicaoPublic,
    RefeicoesPublic,
    RefeicaoUpdate
)
from app.utils import generate_new_account_email, send_email

router = APIRouter()


@router.get(
    "/",
    response_model=RefeicoesPublic,
)
def read_refeicoes(*, session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve refeicoes.
    """

    count_statement = select(func.count()).select_from(Refeicao)
    count = session.exec(count_statement).one()

    statement = select(Refeicao).offset(skip).limit(limit)
    refeicoes = session.exec(statement).all()

    return RefeicoesPublic(data=refeicoes, count=count)


@router.post(
    "/",
    response_model=RefeicaoPublic
)
def create_refeicao(*, session: SessionDep, refeicao_in: RefeicaoCreate) -> Any:
    """
    Create new refeicao.
    """
    refeicao = crud.get_refeicao(session=session,refeicao_id=refeicao_in.id)
    if refeicao:
        raise HTTPException(
            status_code=400,
            detail="The refeicao with this line already exists in the system.",
        )

    refeicao = crud.create_refeicao(session=session, refeicao_create=refeicao_in)
    return refeicao

@router.get(
        "/{refeicao_id}",
        response_model=RefeicaoPublic)
def get_refeicao(*, session: SessionDep, refeicao_id: int) -> Any:
    """
    Delete a refeicao by ID.
    """
    refeicao = crud.get_refeicao(session=session, refeicao_id=refeicao_id)
    if not refeicao:
        raise HTTPException(
            status_code=404,
            detail="Refeicao not found.",
        )
    return refeicao

@router.put(
        "/{refeicao_id}",
        response_model=RefeicaoPublic
)
def update_refeicao(*, session: SessionDep, refeicao_id: int, refeicao_in: RefeicaoUpdate) -> Any:
    """
    Update a refeicao by ID.
    """
    refeicao = crud.get_refeicao(session=session, refeicao_id=refeicao_id)
    if not refeicao:
        raise HTTPException(
            status_code=404,
            detail="Refeicao not found.",
        )

    refeicao = crud.update_refeicao(
        session=session, 
        refeicao_id=refeicao_id, 
        refeicao=refeicao_in
    )
    return refeicao

@router.delete(
        "/{refeicao_id}",
        response_model=RefeicaoPublic
)
def delete_refeicao(*, session: SessionDep, refeicao_id: int) -> Any:
    """
    Delete a refeicao by ID.
    """
    refeicao = crud.get_refeicao(session=session, refeicao_id=refeicao_id)
    if not refeicao:
        raise HTTPException(
            status_code=404,
            detail="Refeicao not found.",
        )

    crud.delete_refeicao(session=session, refeicao_id=refeicao_id)
    return refeicao