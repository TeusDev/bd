import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select,text
from .calorias import calculate_calories 
from app.api.deps import CurrentUser, SessionDep
from app.crud import get_avaliacao
from app.models import (
    Plano,
    PlanoBase,
    PlanoCreate,
    PlanosPublic,
    PlanoUpdate,
    PlanoPublic,
    Avaliacao
)

router = APIRouter()

@router.get("/",response_model=PlanosPublic)
def read_planos ( session: SessionDep, skip: int = 0, limit: int = 100
) -> Any:
    count_statement = select(func.count()).select_from(Plano)
    count = session.exec(count_statement).one()
    statement = select(Plano).offset(skip).limit(limit)
    planos = session.exec(statement).all()
    return PlanosPublic(data=planos,count=count)


@router.post("/", response_model=PlanoPublic)
def create_planos(
    *, session: SessionDep, current_user: CurrentUser, plano_in: PlanoCreate
) -> Any:
    """
    Create new plano.
    """
    avaliacao = get_avaliacao(session=session,id=plano_in.id_avaliacao)
    calorias = calculate_calories(avaliacao=avaliacao)

    procedure_call = text("""
        SELECT id_dieta
        FROM get_dieta_by_max_calories(:calories)
    """)
    result = session.execute(procedure_call, {'calories':calorias}).fetchone()

    if result is None:
        raise ValueError("No dieta found with the given calorie limit")

    id_dieta = result.id_dieta
    
    plano = Plano(
        id=plano_in.id,
        id_user=plano_in.id_dieta,
        id_sessao_treino=plano_in.id_sessao_treino,
        id_treinador=plano_in.id_treinador,
        id_avaliacao=plano_in.id_avaliacao,
        id_dieta=id_dieta
    )
    planes = Plano.model_validate(plano)
    session.add(planes)
    session.commit()
    session.refresh(planes)
    return planes
