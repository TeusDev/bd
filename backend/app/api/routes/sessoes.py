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
    treino_sessao,
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
    INNER JOIN 
        treino_sessao AS ts ON ts.id_sessao = sessao.id
    INNER JOIN 
        treino AS t1 ON t1.id = ts.id_treino1
    INNER JOIN 
        treino AS t2 ON t2.id = ts.id_treino2
    INNER JOIN 
        treino AS t3 ON t3.id = ts.id_treino3
    INNER JOIN 
        treino_exercicio AS te1 ON te1.id_treino = t1.id
    INNER JOIN 
        treino_exercicio AS te2 ON te2.id_treino = t2.id
    INNER JOIN 
        treino_exercicio AS te3 ON te3.id_treino = t3.id
    INNER JOIN 
        exercicio AS e1 ON e1.id = te1.id_exercicio
    INNER JOIN 
        exercicio AS e2 ON e2.id = te2.id_exercicio
    INNER JOIN 
        exercicio AS e3 ON e3.id = te3.id_exercicio
    LIMIT :limit OFFSET :skip
    """)

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
    "/",    dependencies=[Depends(get_current_active_superuser)],response_model=SessaoPublic
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
    treino_1 = crud.get_treinos(session=session, id=treino1)
    if not treino_1:
        raise HTTPException(
            status_code=400,
            detail="The treino with this id doesnt exists in the system.",
        )
        
    treino_2 = crud.get_treinos(session=session, id=treino2)
    if not treino_2:
        raise HTTPException(
            status_code=400,
            detail="The treino with this id doesnt exists in the system.",
        )
        
    treino_3 = crud.get_treinos(session=session, id=treino3)
    if not treino_3:
        raise HTTPException(
            status_code=400,
            detail="The treino with this id doesnt exists in the system.",
        )
    
    sessao = crud.get_sessoes(session=session, id=sessao_in.id)
    if sessao:
        raise HTTPException(
            status_code=400,
            detail="The sessao with this id already exists in the system.",
        )
        
    
    sessao = crud.create_sessao(session=session, sessao_create=sessao_in,treino_ids=[treino1,treino2,treino3])
    
    
    sessao_ref = treino_sessao(
        id_sessao=sessao_in.id,
        id_treino1=treino1,
        id_treino2=treino2,
        id_treino3=treino3
    )
    
      
    stm2 = select(treino_sessao).where(treino_sessao.id_sessao==sessao.id
                                       and treino_sessao.id_treino1==treino1
                                       and treino_sessao.id_treino2==treino2
                                       and treino_sessao.id_treino3==treino3)
    existing_ref = session.exec(stm2).first()
    if existing_ref:
        return Message("Associação entre sessao e treinos ja existe")
    
    session.add(sessao_ref)
    session.commit()
    session.refresh(sessao_ref)


    create_procedure_sql = text("""
        CREATE OR REPLACE FUNCTION get_total_calories(p_id_sessao INTEGER)  -- Renamed parameter
        RETURNS INTEGER AS $$
        DECLARE
            total_calories INTEGER;
        BEGIN
            SELECT COALESCE(t1.calorias, 0) + COALESCE(t2.calorias, 0) + COALESCE(t3.calorias, 0)
            INTO total_calories
            FROM treino_sessao ts
            JOIN treino t1 ON ts.id_treino1 = t1.id
            JOIN treino t2 ON ts.id_treino2 = t2.id
            JOIN treino t3 ON ts.id_treino3 = t3.id
            WHERE ts.id_sessao = p_id_sessao;  -- Use the renamed parameter here

            RETURN total_calories;
        END;
        $$ LANGUAGE plpgsql;
        """)
    
    session.execute(create_procedure_sql)
    session.commit()
    result = session.execute(text(f"SELECT get_total_calories(CAST({sessao_in.id} AS INTEGER))"))
    total_calories = result.scalar()
    exercise_details = get_exercise_details(session, sessao.id)
    sessoes = SessaoPublic(
        id=sessao.id,
        data=sessao_in.data,
        duracao_total=sessao_in.duracao_minutos,
        exercicio1=exercise_details.exercicio1_name,
        exercicio2=exercise_details.exercicio2_name,
        exercicio3=exercise_details.exercicio3_name,
        grupo_muscular1=exercise_details.grupo_muscular1,
        grupo_muscular2=exercise_details.grupo_muscular2,
        grupo_muscular3=exercise_details.grupo_muscular3,
        calorias_gastas=total_calories
    )
    return sessoes

@router.delete("/{sessao}",  dependencies=[Depends(get_current_active_superuser)],)
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

def get_exercise_details(session: SessionDep, sessao_id: int):
    query = text("""
    SELECT 
        e1.exercicio AS exercicio1_name, e1.grupo_muscular AS grupo_muscular1,
        e2.exercicio AS exercicio2_name, e2.grupo_muscular AS grupo_muscular2,
        e3.exercicio AS exercicio3_name, e3.grupo_muscular AS grupo_muscular3
        FROM treino_sessao ts
        JOIN treino_exercicio te1 ON ts.id_treino1 = te1.id_treino
        JOIN exercicio e1 ON te1.id_exercicio = e1.id
        JOIN treino_exercicio te2 ON ts.id_treino2 = te2.id_treino
        JOIN exercicio e2 ON te2.id_exercicio = e2.id
        JOIN treino_exercicio te3 ON ts.id_treino3 = te3.id_treino
        JOIN exercicio e3 ON te3.id_exercicio = e3.id
        WHERE ts.id_sessao = :sessao_id;
    """)
    
    result = session.execute(query, {"sessao_id": sessao_id}).fetchone()
    return result