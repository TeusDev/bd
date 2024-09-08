import uuid
from typing import Any
from sqlmodel import Session, select
import io

from datetime import datetime

from fastapi import (
    APIRouter, 
    HTTPException,
    UploadFile,
    File)

from fastapi.responses import StreamingResponse
from sqlmodel import col, delete, func, select
import re
from app import crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.core.config import settings
from app.core.security import get_password_hash, verify_password

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Shape,
    ShapeBase,
    ShapeCreate,
    ShapeDelete,
    ShapePublic,
    ShapesPublic
)

router = APIRouter()

@router.post("/shapes/", response_model=ShapePublic)
async def create_upload_file(
    session: SessionDep,
    
    current_user: CurrentUser,
    file: UploadFile = File(...)
):
    nome_foto = datetime.now().strftime("capture_%Y%m%d_%H%M%S")

    contents = await file.read()
    new_shape = Shape(nome_foto=nome_foto, foto=contents, usuario_id=current_user.id)
    session.add(new_shape)
    session.commit()
    session.refresh(new_shape)
    return ShapePublic.from_orm(new_shape)

@router.get("/shapes/{shape_id}/foto")
async def get_foto(session: SessionDep, id: int):
    result = session.execute(select(Shape).where(Shape.id == id))
    shape = result.scalars().first()

    if not shape or not shape.foto:
        raise HTTPException(status_code=404, detail="Shape or photo not found")

    return StreamingResponse(io.BytesIO(shape.foto), media_type="image/png")

@router.get("/shapes/fotos")
async def get_fotos(
    session: SessionDep, 
    current_user: CurrentUser
):
    if current_user.is_superuser:
        result = session.execute(select(Shape))
    else:
        result = session.execute(select(Shape).where(Shape.usuario_id == current_user.id))
    
    shapes = result.scalars().all()

    if not shapes:
        raise HTTPException(status_code=404, detail="No shapes or photos found")

    fotos = [{"id": shape.id, "foto": io.BytesIO(shape.foto)} for shape in shapes if shape.foto]
    if not fotos:
        raise HTTPException(status_code=404, detail="No photos available")

    responses = [{"id": foto["id"]} for foto in fotos]

    return responses

@router.get("/shapes/fotos/{user_id}")
async def get_fotos_by_user(
    user_id: int,
    session: SessionDep, 
    current_user: CurrentUser
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Operation not permitted")

    result = session.execute(select(Shape).where(Shape.usuario_id == user_id))
    
    shapes = result.scalars().all()

    if not shapes:
        raise HTTPException(status_code=404, detail="No shapes or photos found for the specified user")

    fotos = [{"id": shape.id, "foto": io.BytesIO(shape.foto)} for shape in shapes if shape.foto]
    if not fotos:
        raise HTTPException(status_code=404, detail="No photos available for the specified user")

    responses = [{"id": foto["id"], "foto": StreamingResponse(foto["foto"], media_type="image/png")} for foto in fotos]

    return responses

@router.delete("/shapes/fotos/{shape_id}")
async def delete_foto(
    shape_id: int,
    session: SessionDep, 
    current_user: CurrentUser
):
    shape = session.get(Shape, shape_id)
    
    if not shape:
        raise HTTPException(status_code=404, detail="Shape not found")
    
    if not current_user.is_superuser and shape.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation not permitted")

    session.delete(shape)
    session.commit()
    
    return {"detail": "Shape deleted successfully"}