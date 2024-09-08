import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select,text
from sqlalchemy.orm import joinedload
from sqlalchemy import text

from app import crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.models import (
    Dieta,
    DietaCreate,
    DietaPublic,
    DietasPublic,
    DietaUpdate,
    Refeicao,
    RefeicaoBase,
    RefeicaoPublic,
    dieta_refeicoes
)
from app.utils import generate_new_account_email, send_email
from typing import Any, List, Dict

router = APIRouter()


@router.get(
    "/",
    response_model=DietasPublic,
)
def read_dietas(session: SessionDep, skip: int = 0, limit: int = 100) -> DietasPublic:
    """
    Retrieve dietas along with their associated refeicoes.
    """
    count_statement = select(func.count()).select_from(Dieta)
    count = session.exec(count_statement).one()
    
    sql_query = text("""
    SELECT 
        dieta.id AS id_dieta,
        r_manha.name AS nome_ref_manha,
        r_tarde.name AS nome_ref_tarde,
        r_noite.name AS nome_ref_noite
    FROM 
        dieta
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
        DietaPublic(
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
    "/",
    response_model=DietaPublic
)
def create_dieta(*, session: SessionDep, dieta_in: DietaCreate,
                id_ref_manha:int,
                id_ref_tarde:int,
                id_ref_noite:int,
) -> Any:
    """
    Create new dieta.
    """
    dieta = crud.get_dieta(session=session, id=dieta_in.id)
    if dieta:
        raise HTTPException(
            status_code=400,
            detail="The dieta with this line already exists in the system.",
        )
    
    refeicao = crud.get_refeicao(session=session,refeicao_id=id_ref_manha)
    if not refeicao:
        raise HTTPException(
            status_code=400,
            detail="The refeicao with this line doesnt exists in the system.",
        )

    refeicao2 = crud.get_refeicao(session=session,refeicao_id=id_ref_tarde)
    if not refeicao2:
            raise HTTPException(
                status_code=400,
                detail="The refeicao with this line doesnt exists in the system.",
            )
    refeicao3 = crud.get_refeicao(session=session,refeicao_id=id_ref_noite)
    if not refeicao3:
            raise HTTPException(
                status_code=400,
                detail="The refeicao with this line doesnt exists in the system.",
            )

    
    dieta = crud.create_dieta(refeicoes_ids=[id_ref_manha,id_ref_tarde,id_ref_noite],session=session,dieta_create=dieta_in)
    sql_query = text("""
    SELECT 
        dieta.id AS id_dieta,
        r_manha.name AS nome_ref_manha,
        r_tarde.name AS nome_ref_tarde,
        r_noite.name AS nome_ref_noite
    FROM 
        dieta
    LEFT JOIN 
        dieta_refeicoes ON dieta.id = dieta_refeicoes.id_dieta
    LEFT JOIN 
        refeicao AS r_manha ON dieta_refeicoes.id_ref_manha = r_manha.id
    LEFT JOIN 
        refeicao AS r_tarde ON dieta_refeicoes.id_ref_tarde = r_tarde.id
    LEFT JOIN 
        refeicao AS r_noite ON dieta_refeicoes.id_ref_noite = r_noite.id
    WHERE 
        dieta.id = :dieta_id
    LIMIT :limit OFFSET :skip
    """)
    result = session.execute(
    sql_query,
    {"dieta_id": dieta_in.id, "limit": 1, "skip": 0}
)
    dietas = [
        DietaPublic(
            id=row[0],
            nome_ref_manha=row[1],
            nome_ref_tarde=row[2],
            nome_ref_noite=row[3]
        )
        for row in result
    ]
    dieta_public = dietas[0]
    return dieta_public

@router.get(
        "/{dieta_id}",
        response_model=DietaPublic)
def get_dieta(*, session: SessionDep, dieta_id: int):
    """
    Retrieve a single dieta by ID.
    """
    sql_query = text("""
    SELECT 
        dieta.id ,
        r_manha.name AS nome_ref_manha,
        r_tarde.name AS nome_ref_tarde,
        r_noite.name AS nome_ref_noite
    FROM 
        dieta
    INNER JOIN 
        dieta_refeicoes ON dieta.id = dieta_refeicoes.id_dieta
    INNER JOIN 
        refeicao AS r_manha ON dieta_refeicoes.id_ref_manha = r_manha.id
    INNER JOIN 
        refeicao AS r_tarde ON dieta_refeicoes.id_ref_tarde = r_tarde.id
    INNER JOIN 
        refeicao AS r_noite ON dieta_refeicoes.id_ref_noite = r_noite.id
    WHERE 
        dieta.id = :dieta_id
    LIMIT :limit OFFSET :skip
""")
    result = session.execute(
    sql_query,
    {"dieta_id": dieta_id, "limit": 1, "skip": 0}
    )
    
    dietas = [
        DietaPublic(
            id=row[0],
            nome_ref_manha=row[1],
            nome_ref_tarde=row[2],
            nome_ref_noite=row[3]
        )
        for row in result
    ]
    dieta_public = dietas[0]
    if not dieta_public:
        raise HTTPException(
            status_code=404,
            detail="Dieta not found."
    )
    return dieta_public

@router.put(
        "/{dieta_id}",
        response_model=DietaPublic
)
def update_dieta(*, session: SessionDep, dieta_id: int, dieta_in: DietaUpdate) -> Any:
    """
    Update a dieta by ID.
    """
    # Fetch the existing dieta record
    dieta = crud.get_dieta(session=session, id=dieta_id)
    if not dieta:
        raise HTTPException(
            status_code=404,
            detail="Dieta not found.",
        )

    # Update dieta_refeicoes with new values
    sql_query = text("""
    UPDATE dieta_refeicoes
    SET 
        id_ref_manha = :id_ref_manha,
        id_ref_tarde = :id_ref_tarde,
        id_ref_noite = :id_ref_noite
    WHERE 
        id_dieta = :dieta_id;
    """)
    session.execute(
        sql_query,
        {
            "id_ref_manha": dieta_in.id_ref_manha,
            "id_ref_tarde": dieta_in.id_ref_tarde,
            "id_ref_noite": dieta_in.id_ref_noite,
            "dieta_id": dieta_id
        }
    )
    session.commit()  # Commit the update

    # Query the updated dieta and associated refeicoes
    sql_query = text("""
    SELECT 
        dieta.id AS id_dieta,
        r_manha.name AS nome_ref_manha,
        r_tarde.name AS nome_ref_tarde,
        r_noite.name AS nome_ref_noite
    FROM 
        dieta
    LEFT JOIN 
        dieta_refeicoes ON dieta.id = dieta_refeicoes.id_dieta
    LEFT JOIN 
        refeicao AS r_manha ON dieta_refeicoes.id_ref_manha = r_manha.id
    LEFT JOIN 
        refeicao AS r_tarde ON dieta_refeicoes.id_ref_tarde = r_tarde.id
    LEFT JOIN 
        refeicao AS r_noite ON dieta_refeicoes.id_ref_noite = r_noite.id
    WHERE 
        dieta.id = :dieta_id
    LIMIT :limit OFFSET :skip
    """)
    result = session.execute(
        sql_query,
        {"dieta_id": dieta_id, "limit": 1, "skip": 0}
    )

    # Use result.mappings() to get the row as a dictionary-like object
    row = result.mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="Dieta not found after update.")

    # Create a DietaPublic object from the row data
    dieta_public = DietaPublic(
        id=row["id_dieta"],
        nome_ref_manha=row["nome_ref_manha"],
        nome_ref_tarde=row["nome_ref_tarde"],
        nome_ref_noite=row["nome_ref_noite"]
    )

    return dieta_public

@router.delete(
        "/{dieta_id}",
        response_model=DietaPublic
)
def delete_dieta(*, session: SessionDep, dieta_id: int) -> Any:
    """
    Delete a dieta by ID.
    """
    dieta = crud.get_dieta(session=session, dieta_id=dieta_id)
    if not dieta:
        raise HTTPException(
            status_code=404,
            detail="Dieta not found.",
    )

    crud.delete_dieta(session=session, dieta_id=dieta_id)
    return dieta