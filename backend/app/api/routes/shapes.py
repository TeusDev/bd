import uuid
from typing import Any
from sqlmodel import Session, select
import io

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
    nome_foto: str,
    file: UploadFile = File(...)
):
    contents = await file.read()
    new_shape = Shape(nome_foto=nome_foto, foto=contents)
    session.add(new_shape)
    session.commit()
    session.refresh(new_shape)

    return ShapePublic.from_orm(new_shape)

@router.get("/shapes/{shape_id}/foto")
async def get_foto(session: SessionDep, nome_foto: str):
    result = session.execute(select(Shape).where(Shape.nome_foto == nome_foto))
    shape = result.scalars().first()

    if not shape or not shape.foto:
        raise HTTPException(status_code=404, detail="Shape or photo not found")

    return StreamingResponse(io.BytesIO(shape.foto), media_type="image/png")