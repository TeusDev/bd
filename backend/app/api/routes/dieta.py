import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select

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
    DietaUpdate
)
from app.utils import generate_new_account_email, send_email

router = APIRouter()


@router.get(
    "/",
    response_model=DietasPublic,
)
def read_dietas(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve dietas.
    """

    count_statement = select(func.count()).select_from(Dieta)
    count = session.exec(count_statement).one()

    statement = select(Dieta).offset(skip).limit(limit)
    dietas = session.exec(statement).all()

    return DietasPublic(data=dietas, count=count)


@router.post(
    "/",
    response_model=DietaPublic
)
def create_dieta(*, session: SessionDep, dieta_in: DietaCreate) -> Any:
    """
    Create new dieta.
    """
    dieta = crud.get_dieta(session=session, dieta_id=dieta_in.id)
    if dieta:
        raise HTTPException(
            status_code=400,
            detail="The dieta with this line already exists in the system.",
        )

    dieta = crud.create_dieta(session=session, dieta_create=dieta_in)
    return dieta

@router.get(
        "/{dieta_id}",
        response_model=DietaPublic)
def get_dieta(*, session: SessionDep, dieta_id: int):
    """
    Retrieve a single dieta by ID.
    """
    dieta = crud.get_dieta(session, dieta_id=dieta_id)
    if not dieta:
        raise HTTPException(
            status_code=404,
            detail="Dieta not found."
        )
    return dieta

@router.put(
        "/{dieta_id}",
        response_model=DietaPublic
)
def update_dieta(*, session: SessionDep, dieta_id: int, dieta_in: DietaUpdate) -> Any:
    """
    Update a dieta by ID.
    """
    dieta = crud.get_dieta(session=session, dieta_id=dieta_id)
    if not dieta:
        raise HTTPException(
            status_code=404,
            detail="Dieta not found.",
        )

    dieta = crud.update_dieta(
        session=session, 
        dieta_id=dieta_id, 
        dieta=dieta_in
    )
    return dieta

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