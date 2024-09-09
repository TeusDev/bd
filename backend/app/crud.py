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
    Refeicao,
    RefeicaoCreate,
    Dieta,
    DietaCreate, 

    TreinadorCreate,
    Treinador,
    Avaliacao,
    AvaliacaoCreate,
    AvaliacaoUpdate,
    Plano,
    PlanoCreate,
    PlanoUpdate,
    Exercicio,
    ExercicioCreate,
    Sessao,
    SessaoCreate,
    Treino,
    TreinoCreate,
    dieta_refeicoes,
    treino_sessao,
    treino_exercicio
)



def create_exercicio(*, session: Session, exercicio_create: ExercicioCreate) -> Exercicio:
    db_obj = Exercicio.model_validate(
        exercicio_create
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def create_treino(*, session: Session, treino_create: TreinoCreate,exercicio:int) -> Treino:
    db_obj = Treino.model_validate(
        treino_create
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    
    # treino_exercicios = treino_exercicio(
    #     id_treino=treino_create.id,
    #     id_exercicio=exercicio
    # )
    # session.add(treino_exercicios)
    # session.commit()
    # session.refresh(treino_exercicios)
    
    return db_obj

def create_sessao(*, session: Session, sessao_create: SessaoCreate,treino_ids:list[int]) -> Sessao:
    db_obj = Sessao.model_validate(
        sessao_create
    )
    
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    
    # sessao_ref = treino_sessao(
    #     id_sessao=db_obj.id,
    #     id_treino1=treino_ids[0],
    #     id_treino2=treino_ids[1],
    #     id_treino3=treino_ids[2]
    # )
    # session.add(sessao_ref)
    # session.commit()
    # session.refresh(sessao_ref)

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

def create_treinador(*, session: Session, treinador_create: TreinadorCreate) -> Treinador | None:
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

def get_exercicios(*, session: Session, id: int) -> Exercicio | None:
    statement = select(Exercicio).where(Exercicio.id == id)
    exercicios = session.exec(statement).first()
    return exercicios

def get_treinos(*, session: Session, id: int) -> Treino | None:
    statement = select(Treino).where(Treino.id == id)
    treinos = session.exec(statement).first()
    return treinos

def get_sessoes(*, session: Session, id: int) -> Sessao | None:
    statement = select(Sessao).where(Sessao.id == id)
    sessoes = session.exec(statement).first()
    return sessoes


def get_treinadores(*, session: Session, id: str) -> Treinador | None:
    statement = select(Treinador).where(Treinador.id == id)
    treinadores = session.exec(statement).first()
    return treinadores

def get_avaliacoes(*, session: Session, id: int) -> Avaliacao | None:
    statement = select(Avaliacao).where(Avaliacao.id == id)
    avaliacoes = session.exec(statement).first()
    return avaliacoes

def get_avaliacao(*, session: Session, id: int):
    avaliacao = session.get(Avaliacao, id)
    return avaliacao

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

##########LUCAS###########################
# TODO: passar paramentros: refeicao_id

def create_refeicao(*, session: Session, refeicao_create: RefeicaoCreate):
    db_obj = Refeicao.model_validate(
        refeicao_create
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def get_refeicoes(*, session: Session, skip: int = 0, limit: int = 10):
    statement = select(Refeicao)
    refeicoes = session.exec(select(statement).offset(skip).limit(limit)).all()
    return refeicoes

def get_refeicao(*, session: Session, refeicao_id: int):
    refeicao = session.get(Refeicao, refeicao_id)
    # statement = select(Refeicao).where(Refeicao.id == id)
    return refeicao



def update_refeicao(*, session: Session, refeicao_id: int, refeicao: Refeicao):
    db_refeicao = session.get(Refeicao, refeicao_id)
    
    for key, value in refeicao.dict(exclude_unset=True).items():
        setattr(db_refeicao, key, value)
    session.add(db_refeicao)
    session.commit()
    session.refresh(db_refeicao)
    return db_refeicao

def delete_refeicao(*, session: Session, refeicao_id: int):
    refeicao = session.get(Refeicao, refeicao_id)
    nullify_dieta_references(refeicao_id)
    session.delete(refeicao)
    session.commit()
    return {"ok": True}


def create_dieta(*, session: Session, dieta_create: DietaCreate, refeicoes_ids: list[int]) -> Dieta:
    db_obj = Dieta.model_validate(
        dieta_create
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)

    # dieta_ref = dieta_refeicoes(
    #     id_dieta=db_obj.id,
    #     id_ref_manha=refeicoes_ids[0],
    #     id_ref_tarde=refeicoes_ids[1],
    #     id_ref_noite=refeicoes_ids[2]
    # )
    # session.add(dieta_ref)
    # session.commit()
    # session.refresh(dieta_ref)
    
    return db_obj
    
def index_dietas(*, session: Session, skip: int = 0, limit: int = 10):
    dietas = session.exec(select(Dieta).offset(skip).limit(limit)).all()
    return dietas

def get_dieta(*, session: Session, id: str):
    dieta = session.get(Dieta, id)
    return dieta

def update_dieta(*, session: Session, dieta_id: str, dieta: Dieta):
    db_dieta = session.get(Dieta, dieta_id)
    for key, value in dieta.dict(exclude_unset=True).items():
        setattr(db_dieta, key, value)
    session.add(db_dieta)
    session.commit()
    session.refresh(db_dieta)
    return db_dieta

def nullify_dieta_references(*, session: Session, refeicao_id: int) -> None:

    # Atualiza as dietas que têm a refeição como referência para NULL
    session.exec(
        update_dieta(Dieta)
        .where(Dieta.id_ref_manha == refeicao_id)
        .values(id_ref_manha=None)
    )
    session.exec(
        update_dieta(Dieta)
        .where(Dieta.id_ref_tarde == refeicao_id)
        .values(id_ref_tarde=None)
    )
    session.exec(
        update_dieta(Dieta)
        .where(Dieta.id_ref_noite == refeicao_id)
        .values(id_ref_noite=None)
    )
    session.commit()

def delete_dieta(*, session: Session, dieta_id: str):
    dieta = session.get(Dieta, dieta_id)
    session.delete(dieta)
    session.commit()
    return {"ok": True}
# def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
#     db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
#     session.add(db_item)
#     session.commit()
#     session.refresh(db_item)
#     return db_item
