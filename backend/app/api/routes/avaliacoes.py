import uuid
from typing import Any,List,Tuple
import random
import io
from fastapi.responses import StreamingResponse

from fastapi import APIRouter, HTTPException,Depends, UploadFile,File
from sqlmodel import func, select, text
from app import crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
import datetime
from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Avaliacao,
    AvaliacaoBase,
    AvaliacaoCreate,
    AvaliacaoPublic,
    AvaliacaoUpdate,
    AvaliacoesPublic,
    Plano,
    Shape,
    Message
)

router = APIRouter()


@router.get("/by_id/{avaliacao_id}", response_model=AvaliacaoPublic)
def read_avaliacao_by_id(
    session: SessionDep, 
    avaliacao_id: int, 
    current_user: CurrentUser
) -> Any:
    """
    Retrieve avaliacao by ID. Check if the current user is the owner of plano where aval is associated.
    """
    # Retrieve the avaliacao by ID
    avaliacao = crud.get_avaliacao(session=session, id=avaliacao_id)
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliacao not found")

    # Retrieve the associated plano
    plano = session.exec(select(Plano).where(Plano.id == avaliacao.plano_id)).first()
    if not plano:
        raise HTTPException(status_code=404, detail="Plano not found")

    # Check if the current user is the owner of the plano or a superuser
    if not current_user.is_superuser and plano.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this avaliacao")

    return avaliacao

@router.get("/read_avaliacoes", response_model=AvaliacoesPublic)
def read_avaliacoes(session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100) -> Any:
    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Avaliacao)
        count = session.exec(count_statement).one()
        statement = select(Avaliacao).offset(skip).limit(limit)
        avaliacoes = session.exec(statement).all()
        return AvaliacoesPublic(data=avaliacoes, count=count)
    else:
        statement = text("""
            SELECT a.id,a.data_avaliacao,a.peso,a.altura,a.perc_gordura,a.shape_id
            FROM avaliacao a
            JOIN shape s ON a.shape_id = s.id
            WHERE s.usuario_id = :current_user_id
            LIMIT :limit OFFSET :skip
        """)

        try:
            result = session.execute(statement, {
                "current_user_id": current_user.id,
                "limit": limit,
                "skip": skip
            }).fetchall()
        except Exception as e:
            raise HTTPException(status_code=500, detail="Database query failed") from e

        avaliacoes = [
            Avaliacao(
                id=row[0],
                data_avaliacao=row[1],
                peso=row[2],
                altura=row[3],
                perc_gordura=row[4],
                shape_id=row[5]
            )
            for row in result
        ] if result else []

        return AvaliacoesPublic(data=avaliacoes, count=len(avaliacoes))

@router.post("/", response_model=AvaliacaoPublic, dependencies=[Depends(get_current_active_superuser)])
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
@router.post("/get_photo_names")
async def get_photo_names(current_user: CurrentUser, session: SessionDep) -> List[Tuple[int, str]]:
    """
    Retrieve all photo names and their IDs associated with the current user.
    """
    shapes = session.query(Shape).filter(Shape.usuario_id == current_user.id).all()
    return [(shape.id, shape.nome_foto) for shape in shapes]


@router.post("/avaliacoes_user", response_model=Message)
async def create_avaliacoes_user(
    current_user: CurrentUser,
    session: SessionDep,
    data_avaliacao: str,
    peso: float,
    altura: float,
    perc_gordura: float,
    photo_id: int,
    available_photos: List[Tuple[int, str]] = Depends(get_photo_names)  
) -> Message:
    """
    Create new avaliacao.
    """
    if photo_id not in [photo[0] for photo in available_photos]: 
        raise HTTPException(status_code=400, detail="Invalid photo ID selected.")

    try:
        datas = datetime.datetime.strptime(data_avaliacao, "%d/%m/%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use dd/mm/yyyy.")

    id = random.randint(0, 10000000)
    existing_avaliacao = crud.get_avaliacoes(session=session, id=id)
    while existing_avaliacao:
        id = random.randint(0, 10000000)
        existing_avaliacao = crud.get_avaliacoes(session=session, id=id)

    avaliacao = Avaliacao(
        id=id,
        data_avaliacao=datas,
        peso=peso,
        altura=altura,
        perc_gordura=perc_gordura,
        shape_id=photo_id  
    )

    session.add(avaliacao)
    session.commit()
    session.refresh(avaliacao)

    return Message(message="Avaliação criada com sucesso")


@router.delete("/{avaliacao_id}",  dependencies=[Depends(get_current_active_superuser)])
def delete_avaliacao(
    *, session: SessionDep, avaliacao_id: int, current_user: CurrentUser
) -> Any:
    """
    Delete avaliacao.
    """
    avaliacao = session.get(Avaliacao, avaliacao_id)
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliacao not found")

    # Check if the current user is the owner of the avaliacao or a superuser
    if not current_user.is_superuser and avaliacao.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this avaliacao")

    session.delete(avaliacao)
    session.commit()
    return {"message": "Avaliacao deleted"}
