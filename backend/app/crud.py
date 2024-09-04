import uuid
from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import (
    # Item, 
    # ItemCreate, 
    User, 
    UserCreate, 
    UserUpdate, 
    Telefone, 
    TelefoneCreate,
    TreinadorCreate,
    Treinador,
    Avaliacao,
    AvaliacaoCreate,
    AvaliacaoUpdate,
    Plano,
    PlanoCreate,
    PlanoUpdate
)

def create_telefone(*, session: Session, telefone_create: TelefoneCreate) -> Telefone:
    db_obj = Telefone.model_validate(
        telefone_create
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def create_avaliacao(*,session:Session,avaliacao_create:AvaliacaoCreate) -> Avaliacao:
    db_obj = Avaliacao.model_validate(
        avaliacao_create
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def create_plano(*,session:Session,plano_create:PlanoCreate) -> Plano:
    db_obj = Plano.model_validate(
        plano_create
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def create_treinador(*, session: Session, treinador_create: TreinadorCreate) -> Treinador:
    db_obj = Treinador.model_validate(
        treinador_create
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user




def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user

def get_telefones(*, session: Session, telefone: str) -> Telefone | None:
    statement = select(Telefone).where(Telefone.telefone == telefone)
    telefones = session.exec(statement).first()
    return telefones

def get_treinadores(*, session: Session, telefone: str) -> Treinador | None:
    statement = select(Treinador).where(Treinador.telefone == telefone)
    treinadores = session.exec(statement).first()
    return treinadores

def get_avaliacoes(*, session: Session, id: int) -> Avaliacao | None:
    statement = select(Avaliacao).where(Avaliacao.id == id)
    avaliacoes = session.exec(statement).first()
    return avaliacoes

def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


# def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
#     db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
#     session.add(db_item)
#     session.commit()
#     session.refresh(db_item)
#     return db_item
