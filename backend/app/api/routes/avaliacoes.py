import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Avaliacao,
    AvaliacaoBase,
    AvaliacaoCreate,
    AvaliacaoPublic,
    AvaliacaoUpdate,
    AvaliacoesPublic
)

router = APIRouter()

@router.get("/",response_model=AvaliacoesPublic)
def read_avaliacoes ( session: SessionDep, skip: int = 0, limit: int = 100
) -> Any:
    count_statement = select(func.count()).select_from(Avaliacao)
    count = session.exec(count_statement).one()
    statement = select(Avaliacao).offset(skip).limit(limit)
    avaliacoes = session.exec(statement).all()
    return AvaliacoesPublic(data=avaliacoes,count=count)


@router.post("/", response_model=AvaliacaoPublic)
def create_avaliacoes(
    *, session: SessionDep, aval_in: AvaliacaoCreate
) -> Any:
    """
    Create new avaliacao.
    """
    aval = Avaliacao.model_validate(aval_in)
    session.add(aval)
    session.commit()
    session.refresh(aval)
    return aval
