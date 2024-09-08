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

    create_procedure_sql = """
        CREATE OR REPLACE FUNCTION get_dieta_by_max_calories(calories NUMERIC)
        RETURNS TABLE(id_dieta INT) AS $$
        BEGIN
            RETURN QUERY
            SELECT dr.id_dieta
            FROM dieta_refeicoes dr
            JOIN refeicao r_manha ON dr.id_ref_manha = r_manha.id
            JOIN refeicao r_tarde ON dr.id_ref_tarde = r_tarde.id
            JOIN refeicao r_noite ON dr.id_ref_noite = r_noite.id
            GROUP BY dr.id_dieta
            HAVING SUM(r_manha.calories + r_tarde.calories + r_noite.calories) <= calories
            ORDER BY SUM(r_manha.calories + r_tarde.calories + r_noite.calories) DESC
            LIMIT 1;
        END;
        $$ LANGUAGE plpgsql;
        """
    session.execute(create_procedure_sql)
    session.commit()
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
