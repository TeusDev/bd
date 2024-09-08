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

@router.get("/me", response_model=AvaliacoesPublic)


@router.get("/by_id/{avaliacao_id}", response_model=AvaliacaoPublic)
def read_avaliacao_by_id(
    session: SessionDep, 
    avaliacao_id: int, 
    current_user: CurrentUser
) -> Any:
    """
    Retrieve avaliacao by ID. Check if the current user is the owner of plano where aval is associated.
    """
    # Retrieve the avaliacao by ID
    avaliacao = crud.get_avaliacao(session=session, id=avaliacao_id)
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliacao not found")

    # Retrieve the associated plano
    plano = session.exec(select(Plano).where(Plano.id == avaliacao.plano_id)).first()
    if not plano:
        raise HTTPException(status_code=404, detail="Plano not found")

    # Check if the current user is the owner of the plano or a superuser
    if not current_user.is_superuser and plano.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this avaliacao")

    return avaliacao

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

@router.delete("/{avaliacao_id}")
def delete_avaliacao(
    *, session: SessionDep, avaliacao_id: int, current_user: CurrentUser
) -> Any:
    """
    Delete avaliacao.
    """
    avaliacao = session.get(Avaliacao, avaliacao_id)
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliacao not found")

    # Check if the current user is the owner of the avaliacao or a superuser
    if not current_user.is_superuser and avaliacao.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this avaliacao")

    session.delete(avaliacao)
    session.commit()
    return {"message": "Avaliacao deleted"}