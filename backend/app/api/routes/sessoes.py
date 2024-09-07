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
    Sessao,
    SessaoCreate,
    SessaoPublic,
    SessoesPublic,
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
    response_model=SessoesPublic
)
def read_sessoes(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve sessoes de treino.
    """
    count_statement = select(func.count()).select_from(Sessao)
    count = session.exec(count_statement).one()

    sql_query = text("""
   SELECT 
    sessao.id AS sessao_id,
    sessao.data AS sessao_data,
    sessao.duracao_minutos AS duracao_total,
    e1.exercicio AS exercicio1,
    e2.exercicio AS exercicio2,
    e3.exercicio AS exercicio3,
    e1.grupo_muscular AS grupo_muscular1,
    e2.grupo_muscular AS grupo_muscular2,
    e3.grupo_muscular AS grupo_muscular3,
    COALESCE(t1.calorias, 0) + COALESCE(t2.calorias, 0) + COALESCE(t3.calorias, 0) AS calorias_gastas_total
FROM 
    sessao
LEFT JOIN 
    treino_sessao AS ts ON ts.id_sessao = sessao.id
LEFT JOIN 
    treino_exercicio AS te1 ON te1.id_treino = ts.id_treino1
LEFT JOIN 
    treino_exercicio AS te2 ON te2.id_treino = ts.id_treino2
LEFT JOIN 
    treino_exercicio AS te3 ON te3.id_treino = ts.id_treino3
LEFT JOIN 
    exercicio AS e1 ON e1.id = te1.id_exercicio
LEFT JOIN 
    exercicio AS e2 ON e2.id = te2.id_exercicio
LEFT JOIN 
    exercicio AS e3 ON e3.id = te3.id_exercicio
LEFT JOIN 
    treino AS t1 ON t1.id = ts.id_treino1
LEFT JOIN 
    treino AS t2 ON t2.id = ts.id_treino2
LEFT JOIN 
    treino AS t3 ON t3.id = ts.id_treino3
LIMIT :limit OFFSET :skip""")

    results = session.execute(sql_query, {"limit": limit, "skip": skip}).all()

    sessoes = [
        SessaoPublic(
            id=row[0],
            data=row[1],
            duracao_total=row[2],
            exercicio1=row[3],
            exercicio2=row[4],
            exercicio3=row[5],
            grupo_muscular1=row[6],
            grupo_muscular2=row[7],
            grupo_muscular3=row[8],
            calorias_gastas=row[9]
        )
        for row in results
    ]

    # Criar e retornar a instância de DietasPublic
    return SessoesPublic(data=sessoes, count=count)



@router.post(
    "/",response_model=SessaoPublic
)
def create_sessao(*, session: SessionDep, 
                  sessao_in: SessaoCreate,
                  treino1: int,
                  treino2: int,
                  treino3: int
                  ) -> Any:
    """
    Create new sessao.
    """
    treino1 = crud.get_treinos(session=session, id=treino1)
    if not treino1:
        raise HTTPException(
            status_code=400,
            detail="The treino with this id doesnt exists in the system.",
        )
        
    treino2 = crud.get_treinos(session=session, id=treino2)
    if not treino2:
        raise HTTPException(
            status_code=400,
            detail="The treino with this id doesnt exists in the system.",
        )
        
    treino3 = crud.get_treinos(session=session, id=treino3)
    if not treino3:
        raise HTTPException(
            status_code=400,
            detail="The treino with this id doesnt exists in the system.",
        )
    
    sessao = crud.get_sessoes(session=session, id=sessao_in.id)
    if sessao:
        raise HTTPException(
            status_code=400,
            detail="The treino with this id already exists in the system.",
        )
        
    
    sessao = crud.create_sessao(session=session, sessao_create=sessao_in,treino_ids=[treino1,treino2,treino3])
    return sessao

@router.delete("/{sessao}")
def delete_sessao(
    session: SessionDep, id: str
) -> Message:
    """
    Delete a treino.
    """
    sessao = session.get(Sessao, id)
    if not sessao:
        raise HTTPException(status_code=404, detail="Sessao not found")
    session.delete(sessao)
    session.commit()
    return Message(message="Sessao deleted successfully")

