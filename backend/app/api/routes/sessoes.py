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
    sql_query = text("""
    SELECT 
        sessao.id,
        exercicio.name AS exercicio1,
        exercicio.name AS exercicio2,
        exercicio.name AS exercicio3,
        calorias_gastas AS sum(treino1.calorias,treino2.calorias,treino3.calorias)
    FROM 
        sessao
    LEFT JOIN 
        dieta_refeicoes ON dieta.id = dieta_refeicoes.id_dieta
    LEFT JOIN 
        refeicao AS r_manha ON dieta_refeicoes.id_ref_manha = r_manha.id
    LEFT JOIN 
        refeicao AS r_tarde ON dieta_refeicoes.id_ref_tarde = r_tarde.id
    LEFT JOIN 
        refeicao AS r_noite ON dieta_refeicoes.id_ref_noite = r_noite.id
    LIMIT :limit OFFSET :skip
    """)

    results = session.execute(sql_query, {"limit": limit, "skip": skip}).all()

    dietas = [
        SessaoPublic(
            id=row[0],
            nome_ref_manha=row[1],
            nome_ref_tarde=row[2],
            nome_ref_noite=row[3]
        )
        for row in results
    ]

    # Criar e retornar a instância de DietasPublic
    return DietasPublic(data=dietas, count=count)



@router.post(
    "/",response_model=SessaoPublic
)
def create_treino(*, session: SessionDep, sessao_in: SessaoCreate) -> Any:
    """
    Create new sessao.
    """
    treino = crud.get_treinos(session=session, id=sessao_in.id_treino)
    if not treino:
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
        
        
    sessao = crud.create_sessao(session=session, sessao_create=sessao_in)
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

