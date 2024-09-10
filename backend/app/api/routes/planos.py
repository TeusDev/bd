import uuid
from typing import Any
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.core.security import get_password_hash, verify_password

from fastapi import APIRouter, HTTPException,Depends
from sqlmodel import func, select,text
from app.api.deps import CurrentUser, SessionDep
from app.crud import get_avaliacao
from app.models import (
    Plano,
    PlanoBase,
    PlanoCreate,
    PlanosPublic,
    PlanoUpdate,
    PlanoPublic,
    Avaliacao,
    Message,  
    User,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
    Sessao,
    Treinador,Dieta
)

router = APIRouter()

@router.get("/",response_model=PlanosPublic)
def read_planos (current_user: CurrentUser,session: SessionDep, skip: int = 0, limit: int = 100
) -> Any:
    if current_user.is_superuser:     
        count_statement = select(func.count()).select_from(Plano)
        count = session.exec(count_statement).one()
        statement = select(Plano).offset(skip).limit(limit)
        planos = session.exec(statement).all()
        return PlanosPublic(data=planos,count=count)
    
    count_statement = select(func.count()).select_from(Plano).where(Plano.id_user==current_user.id)
    count = session.exec(count_statement).one()
    statement = select(Plano).where(Plano.id_user==current_user.id).offset(skip).limit(limit)
    planos = session.exec(statement).all()
    return PlanosPublic(data=planos,count=count)


@router.post("/", response_model=PlanoPublic)
def create_planos(
    *, session: SessionDep, current_user: CurrentUser, plano_in: PlanoCreate
) -> Any:
    """
    Create new plano.
    """
    avaliacao = get_avaliacao(session=session,id=plano_in.id_avaliacao)

    create_procedure_sql = text("""
  CREATE OR REPLACE FUNCTION get_dieta_by_min_calories()
RETURNS TABLE(id_dieta INT) AS $$
DECLARE
    calorias_limit NUMERIC;  -- Renomeie para evitar ambiguidade
BEGIN
    calorias_limit := 2000;  -- Exemplo de valor fixo para o limite de calorias

    RETURN QUERY
 SELECT dr.id_dieta
FROM dieta_refeicoes dr
JOIN refeicao r_manha ON dr.id_ref_manha = r_manha.id
JOIN refeicao r_tarde ON dr.id_ref_tarde = r_tarde.id
JOIN refeicao r_noite ON dr.id_ref_noite = r_noite.id
GROUP BY dr.id_dieta
HAVING SUM(r_manha.calorias + r_tarde.calorias + r_noite.calorias) <= SUM(calorias_limit)
ORDER BY SUM(r_manha.calorias + r_tarde.calorias + r_noite.calorias) ASC
LIMIT 1;
END;
$$ LANGUAGE plpgsql;
        """)
    session.execute(create_procedure_sql)
    session.commit()
    id_dieta = get_dieta_by_min_calorias(session=session)

    plano = Plano(
        id=plano_in.id,
        id_user=current_user.id,
        id_sessao_treino=plano_in.id_sessao_treino,
        id_treinador=plano_in.id_treinador,
        id_avaliacao=plano_in.id_avaliacao,
        id_dieta=id_dieta
    )
    
        # Corrected query execution
    planez = session.execute(select(Plano).where(Plano.id == plano_in.id)).first()
    if planez:
        raise HTTPException(status_code=404, detail="Plano exists with this id")
    
      
        # Corrected query execution
    userz = session.execute(select(User).where(User.id == current_user.id)).first()
    if not userz:
        raise HTTPException(status_code=404, detail="there is no user with this id")
    
    
      
        # Corrected query execution
    sessoz = session.execute(select(Sessao).where(Sessao.id == plano_in.id_sessao_treino)).first()
    if not sessoz:
        raise HTTPException(status_code=404, detail="Sessoes doesnt exists with this id")
    
      
        # Corrected query execution
    t = session.execute(select(Treinador).where(Treinador.id == plano_in.id_treinador)).first()
    if not t:
        raise HTTPException(status_code=404, detail="Treinador doesnt exists with this id")
    
      
        # Corrected query execution
    av = session.execute(select(Avaliacao).where(Avaliacao.id == plano_in.id_avaliacao)).first()
    if not av:
        raise HTTPException(status_code=404, detail="Avaliacao doesnt exists with this id")
    
      
        # Corrected query execution
    dietazs = session.execute(select(Dieta).where(Dieta.id == id_dieta)).first()
    if not dietazs:
        raise HTTPException(status_code=404, detail="Dieta doesnt exists with this id")
    
    
    session.add(plano)
    session.commit()
    session.refresh(plano)
    return plano

@router.put("/planos/{plano_id}", response_model=PlanoPublic)
def update_plano(
    session: SessionDep,
    current_user: CurrentUser,
    plano_id: int,
    plano_in: PlanoUpdate
) -> Any:
    """
    Update an existing Plano.
    """
    plano = session.query(Plano).filter(Plano.id == plano_id).first()

    if plano.id_user != current_user.id:
        raise HTTPException(status_code=404, detail="Cant edit a plano that is not yours")
    
    if not plano:
        raise HTTPException(status_code=404, detail="Plano not found")
    
    for key, value in plano_in.dict(exclude_unset=True).items():
        setattr(plano, key, value)

    # Commit the changes to the database
    session.commit()
    session.refresh(plano)

    # Return the updated Plano
    return PlanoPublic.from_orm(plano)

def get_dieta_by_min_calorias(session: SessionDep):
    # Chama o procedimento armazenado sem passar parâmetros
    procedure_call = text("""
        SELECT id_dieta
        FROM get_dieta_by_min_calories()
    """)
    result = session.execute(procedure_call).fetchone()

    if result is None:
        raise ValueError("No dieta found with the minimum calorie limit")

    return result[0]  # Retorna o id_dieta

@router.delete("/{id}")
def delete_plano(
    *,session: SessionDep, id: int,current_user:CurrentUser
) -> Message:
    """
    Delete uma plano.
    """
    plano = session.get(Plano, id)
    if plano.id_user != current_user.id:
        raise HTTPException(status_code=404, detail="Cant edit a plano that is not yours")
    
    if not plano:
        raise HTTPException(status_code=404, detail="Plano not found")
    session.delete(plano)
    session.commit()
    return Message(message="Plano deleted successfully")
