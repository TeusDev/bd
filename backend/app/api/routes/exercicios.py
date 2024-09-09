import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
<<<<<<< HEAD
from sqlmodel import col, delete, func, select
=======
from sqlmodel import col, delete, func, select,text
>>>>>>> merge-jp-lucas-teusdev-thfer
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
<<<<<<< HEAD
=======
    ExercicioQueryPublic,
    ExerciciosQueryPublic,
>>>>>>> merge-jp-lucas-teusdev-thfer
    ExerciciosPublic,
    Message
)
from app.utils import generate_new_account_email, send_email

router = APIRouter()


@router.get(
    "/",
    response_model=ExerciciosPublic
)
def read_exercicios(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve exercicios.
    """

    count_statement = select(func.count()).select_from(Exercicio)
    count = session.exec(count_statement).one()

    statement = select(Exercicio).offset(skip).limit(limit)
    exercicios = session.exec(statement).all()

    return ExerciciosPublic(data=exercicios, count=count)


@router.post(
    "/",response_model=ExercicioPublic
)
def create_exercicio(*, session: SessionDep, exercicio_in: ExercicioCreate) -> Any:
    """
    Create new exercicio.
    """
    exercicio = crud.get_exercicios(session=session, id=exercicio_in.id)
    if exercicio:
        raise HTTPException(
            status_code=400,
            detail="The exercicio with this id already exists in the system.",
        )
        
    exercicio = crud.create_exercicio(session=session, exercicio_create=exercicio_in)
    return exercicio

@router.delete("/{exercicio}")
def delete_exercicio(
    session: SessionDep, id: str
) -> Message:
    """
    Delete a exercicio.
    """
    exercicio = session.get(Exercicio, id)
    if not exercicio:
        raise HTTPException(status_code=404, detail="exercicio not found")
    session.delete(exercicio)
    session.commit()
    return Message(message="Exercicio deleted successfully")

<<<<<<< HEAD
=======


def create_view_por_grupos(session: SessionDep):
    """
    Create a view that filters exercises for the muscle group 'Pernas' in any context.
    """
    create_view_sql = text("""
        CREATE OR REPLACE VIEW exercicios_com_pernas AS
        SELECT exercicio, grupo_muscular,id
        FROM exercicio
        WHERE grupo_muscular ILIKE '%Pernas%';    """)
    session.execute(create_view_sql)
    session.commit()

def get_exercicios_com_pernas(session: SessionDep) -> ExerciciosQueryPublic:
    """
    Retrieve exercicios from the view for any context containing 'Pernas'.
    """
    # Criando a view que filtra por 'Pernas'
    create_view_por_grupos(session)
    
    # Query para buscar os exercícios da view
    query = text("""
        SELECT id,exercicio, grupo_muscular
        FROM exercicios_com_pernas
    """)
    result = session.execute(query)
    exercicios = result.fetchall()

    # Convertendo os resultados para instâncias de ExercicioPublic
    exercicios_list = [ExercicioQueryPublic(id=row[0],exercicio=row[1], grupo_muscular=row[2]) for row in exercicios]
    
    # Contando os exercícios
    count_query = text("""
        SELECT COUNT(*)
        FROM exercicios_com_pernas
    """)
    count_result = session.execute(count_query)
    count = count_result.scalar()
    
    # Retornando os resultados
    return ExerciciosQueryPublic(data=exercicios_list, count=count)

# Exemplo de uso
@router.get(
    "/exercicios_com_pernas",
    response_model=ExerciciosQueryPublic
)
def read_exercicios_com_pernas(session: SessionDep) -> ExerciciosQueryPublic:
    """
    Retrieve exercicios for any context containing 'Pernas' from the view.
    """
    return get_exercicios_com_pernas(session)






def create_view_cardio(session: SessionDep):
    """
    Create a view that filters exercises for the muscle group 'Cardio' in any context.
    """
    create_view_sql = text("""
        CREATE OR REPLACE VIEW exercicios_cardio AS
        SELECT exercicio, grupo_muscular,id
        FROM exercicio
        WHERE grupo_muscular ILIKE '%Cardio%';    """)
    session.execute(create_view_sql)
    session.commit()

def get_exercicios_cardio(session: SessionDep) -> ExerciciosQueryPublic:
    """
    Retrieve exercicios from the view for any context containing 'Cardio'.
    """
    create_view_cardio(session)
    
    query = text("""
        SELECT id,exercicio, grupo_muscular
        FROM exercicios_cardio
    """)
    result = session.execute(query)
    exercicios = result.fetchall()

    exercicios_list = [ExercicioQueryPublic(id=row[0],exercicio=row[1], grupo_muscular=row[2]) for row in exercicios]
    
    count_query = text("""
        SELECT COUNT(*)
        FROM exercicios_cardio
    """)
    count_result = session.execute(count_query)
    count = count_result.scalar()
    
    return ExerciciosQueryPublic(data=exercicios_list, count=count)

@router.get(
    "/exercicios_cardio",
    response_model=ExerciciosQueryPublic
)
def read_exercicios_cardio(session: SessionDep) -> ExerciciosQueryPublic:
    """
    Retrieve exercicios for any context containing 'Cardio' from the view.
    """
    return get_exercicios_cardio(session)
>>>>>>> merge-jp-lucas-teusdev-thfer
