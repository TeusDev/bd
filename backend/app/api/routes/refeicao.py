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
    RefeicaoPublic
)
from app.utils import generate_new_account_email, send_email

router = APIRouter()


@router.get(
    "/",
    response_model=RefeicaoPublic,
)
def read_refeicoes(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve refeicoes.
    """

    count_statement = select(func.count()).select_from(Refeicao)
    count = session.exec(count_statement).one()

    statement = select(Refeicao).offset(skip).limit(limit)
    refeicoes = session.exec(statement).all()

    return RefeicaoPublic(data=refeicoes, count=count)


@router.post(
    "/",response_model=RefeicaoPublic
)
def create_refeicao(*, session: SessionDep, refeicao_in: RefeicaoCreate) -> Any:
    """
    Create new refeicao.
    """
    refeicao = crud.get_refeicoes(session=session, refeicao=refeicao_in.refeicao)
    if refeicao:
        raise HTTPException(
            status_code=400,
            detail="The refeicao with this line already exists in the system.",
        )

    refeicao = crud.create_refeicao(session=session, refeicao_create=refeicao_in)
    return refeicao
