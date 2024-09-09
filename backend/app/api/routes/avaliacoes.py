import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select, text
from sqlalchemy import text

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Avaliacao,
    AvaliacaoBase,
    AvaliacaoCreate,
    AvaliacaoPublic,
    AvaliacaoUpdate,
    AvaliacoesPublic,
    Plano,
    Message
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

@router.put("/avaliacoes/{avaliacao_id}", response_model=AvaliacaoPublic)
def update_avaliacao(
    session: SessionDep,
    avaliacao_id: int,
    aval_in: AvaliacaoUpdate
) -> Any:
    """
    Update an existing avaliacao.
    """
    avaliacao = session.query(Avaliacao).filter(Avaliacao.id == avaliacao_id).first()

    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliacao not found")

    for key, value in aval_in.dict(exclude_unset=True).items():
        setattr(avaliacao, key, value)

    # Commit the changes to the database
    session.commit()
    session.refresh(avaliacao)

    # Return the updated Avaliacao
    return AvaliacaoPublic.from_orm(avaliacao)

@router.put(
        "/{avaliacao_id}",
        response_model=AvaliacaoPublic
)
def update_avaliacao(*, session: SessionDep, avaliacao_id: int, avaliacao_in: AvaliacaoUpdate) -> Any:
    """
    Update a avaliacao by ID, including updating the name and calorias.
    """
    avaliacao = session.query(Avaliacao).filter(Avaliacao.id == avaliacao_id).first()
    if not avaliacao:
        raise HTTPException(
            status_code=404,
            detail="Avaliacao not found.",
        )

    # Update the avaliacao record
    sql_query = text("""
    UPDATE avaliacao
    SET data_avaliacao = :data_avaliacao,
        peso = :peso,
        altura = :altura,
        perc_gordura = :perc_gordura
    WHERE id = :avaliacao_id;
    """)
    session.execute(
        sql_query,
        {
            "data_avaliacao" : avaliacao_in.data_avaliacao,
            "peso" : avaliacao_in.peso,
            "altura" : avaliacao_in.altura,
            "perc_gordura" : avaliacao_in.perc_gordura,
            "avaliacao_id": avaliacao_id
        }
    )
    session.commit()

    updated_avaliacao = session.query(Avaliacao).filter(Avaliacao.id == avaliacao_id).first()
    return updated_avaliacao

def delete_avaliacao(
    session: SessionDep,
    avaliacao_id: int
) -> Message:
    """
    Delete an avaliacao and update id_avaliacao in Plano to NULL.
    """
    avaliacao = session.query(Avaliacao).filter(Avaliacao.id == avaliacao_id).first()

    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliacao not found")

    # Atualizar id_avaliacao para NULL em Plano onde id_avaliacao referencia esta Avaliacao
    # planos = session.query(Plano).filter(Plano.id_avaliacao == avaliacao_id).all()
    # for plano in planos:
    #     plano.id_avaliacao = None
    # session.commit()
    #  -----------OR---------
    sql_query = text("""
        UPDATE plano
        SET id_avaliacao = NULL
        WHERE id_avaliacao = :avaliacao_id;
    """)
    session.execute(
        sql_query,
        {
            "avaliacao_id": avaliacao_id
        }
    )

    # Excluir a avaliação
    session.delete(avaliacao)
    session.commit()

    return  Message(message="Deleted avalicacao")