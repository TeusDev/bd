import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select,text
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
    treino_exercicio,
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

    sql_query = text("""
    SELECT 
        t.id AS id_treino,
        te.id_exercicio AS id_exercicio,
        t.calorias
    FROM 
        treino AS t
    LEFT JOIN 
        treino_exercicio AS te ON t.id = te.id_treino
    LEFT JOIN 
        exercicio AS e ON te.id_exercicio = e.id
    LIMIT :limit OFFSET :skip
    """)

    results = session.execute(sql_query, {"limit": limit, "skip": skip}).all()

    treinos = [
        TreinoPublic(
            id=row[0],
            id_exercicio=row[1],
            calorias=row[2]
        )
        for row in results
    ]

    return TreinosPublic(data=treinos, count=count)


@router.post(
    "/",response_model=TreinoPublic
)
def create_treino(*, session: SessionDep, treino_in: TreinoCreate,exercicio_id:int) -> Any:
    """
    Create new treino.
    """
     
    treino1 = crud.get_treinos(session=session, id=treino_in.id)
    if treino1:
        raise HTTPException(
            status_code=400,
            detail="The treino with this id already exists in the system.",
        )
    ex = crud.get_exercicios(session=session,id=exercicio_id)
    if not ex:
         raise HTTPException(
            status_code=400,
            detail="The exercicio with this id doesnt exists in the system.",
        )
    treino = crud.create_treino(session=session, treino_create=treino_in,exercicio=exercicio_id)
    
    treino_exercicios = treino_exercicio(
        id_treino=treino_in.id,
        id_exercicio=exercicio_id
    )
    
    statement = select(treino_exercicio).where(treino_exercicio.id_treino == treino_in.id
                                               and treino_exercicio.id_exercicio==exercicio_id)
    warnings = session.exec(statement).first()
    if warnings:
        return Message(Message="relacao entre treino e exercicio ja existe")
    
    session.add(treino_exercicios)
    session.commit()
    session.refresh(treino_exercicios)
    
    
    treinoz = TreinoPublic(
        id=treino_in.id,
        id_exercicio=exercicio_id,
        calorias=treino_in.calorias
    )
    return treinoz

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

