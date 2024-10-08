import uuid
from typing import Any
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
import random
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
    viewPlano,
    Plan,
    Shape,
    Sessao,
    Treinador,Dieta
)

router = APIRouter()
@router.get("/viewplanos",response_model=viewPlano)
def view_planos (current_user: CurrentUser,session: SessionDep, skip: int = 0, limit: int = 100
) -> Any:
    
    """
    Retrieve a query of planos.
    """
    
    if current_user.is_superuser:
        sql_query = text("""
        SELECT 
            plano.id,
            usuarios.id,
            usuarios.name,
            sessao.duracao_minutos,
            sessao.data,
            treinador.name,
            treinador.telefone,
            treinador.especialidade, 
            avaliacao.peso,
            avaliacao.altura,
            avaliacao.perc_gordura,
            avaliacao.shape_id
        FROM 
            plano
        INNER JOIN 
            "user" as usuarios ON usuarios.id = plano.id_user
        LEFT JOIN 
            sessao ON sessao.id = plano.id_sessao_treino
        LEFT JOIN 
            treinador ON treinador.id = plano.id_treinador
        LEFT JOIN 
            avaliacao ON plano.id_avaliacao = avaliacao.id
        LIMIT :limit OFFSET :skip
    """)  
        
        result = session.execute(
        sql_query,{"limit": limit, "skip": skip}
        )
        
        planos = [Plan(
                plano_id=row[0],
                usuarios_id=row[1],
                user_name=row[2],
                sessao_duracao_minutos=row[3],
                sessao_data=row[4] if row[4] is not None else None,
                treinador_name=row[5] if row[5] is not None else None,
                treinador_telefone=row[6] if row[6] is not None else None,
                treinador_especialidade=row[7] if row[7] is not None else None,
                avaliacao_peso=row[8] if row[8] is not None else None,
                avaliacao_altura=row[9] if row[9] is not None else None,
                avaliacao_perc_gordura=row[10] if row[10] is not None else None,
                avaliacao_shape_id=row[11] if row[11] is not None else None
            )
            for row in result
        ]
        plano_public = planos[0]
        if not plano_public:
            raise HTTPException(
                status_code=404,
                detail="Plano not found."
        )
            
            
        return viewPlano(data=planos)
    sql_query = text("""
        SELECT 
            plano.id,
            usuarios.id,
            usuarios.name,
            sessao.duracao_minutos,
            sessao.data,
            treinador.name,
            treinador.telefone,
            treinador.especialidade, 
            avaliacao.peso,
            avaliacao.altura,
            avaliacao.perc_gordura,
            avaliacao.shape_id
        FROM 
            plano
        INNER JOIN 
            "user" as usuarios ON usuarios.id = plano.id_user
        LEFT JOIN 
            sessao ON sessao.id = plano.id_sessao_treino
        LEFT JOIN 
            treinador ON treinador.id = plano.id_treinador
        LEFT JOIN 
                    avaliacao ON plano.id_avaliacao = avaliacao.id
        WHERE 
        usuarios.id = :id_user
        LIMIT :limit OFFSET :skip
    """)  
        
    result = session.execute(
        sql_query,{"id_user":current_user.id,"limit": limit, "skip": skip}
        )

    planos = [Plan(
                plano_id=row[0],
                usuarios_id=row[1],
                user_name=row[2],
                sessao_duracao_minutos=row[3],
                sessao_data=row[4] if row[4] is not None else None,
                treinador_name=row[5] if row[5] is not None else None,
                treinador_telefone=row[6] if row[6] is not None else None,
                treinador_especialidade=row[7] if row[7] is not None else None,
                avaliacao_peso=row[8] if row[8] is not None else None,
                avaliacao_altura=row[9] if row[9] is not None else None,
                avaliacao_perc_gordura=row[10] if row[10] is not None else None,
                avaliacao_shape_id=row[11] if row[11] is not None else None
            )
            for row in result
        ]
    
    if not planos:
            raise HTTPException(
                status_code=404,
                detail="Plano not found."
        )
            
    plano_public = planos[0]
    if not plano_public:
            raise HTTPException(
                status_code=404,
                detail="Plano not found."
        )
            
            
    return viewPlano(data=planos)
    

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

@router.post("/planos_create", response_model=PlanoPublic, dependencies=[Depends(get_current_active_superuser)])
def create_planos(
    *, session: SessionDep, current_user: CurrentUser, plano_in: PlanoCreate,id_dieta:int
) -> Any:
    """
    Create new plano.
    """
   
    plano = Plano(
        id=plano_in.id,
        id_user=current_user.id,
        id_sessao_treino=plano_in.id_sessao_treino,
        id_treinador=plano_in.id_treinador,
        id_avaliacao=plano_in.id_avaliacao,
        id_dieta=id_dieta
    )
    
    planez = session.execute(select(Plano).where(Plano.id == plano_in.id)).first()
    if planez:
        raise HTTPException(status_code=404, detail="Plano exists with this id")
    
    userz = session.execute(select(User).where(User.id == current_user.id)).first()
    if not userz:
        raise HTTPException(status_code=404, detail="there is no user with this id")
    
    sessoz = session.execute(select(Sessao).where(Sessao.id == plano_in.id_sessao_treino)).first()
    if not sessoz:
        raise HTTPException(status_code=404, detail="Sessoes doesnt exists with this id")
          
    t = session.execute(select(Treinador).where(Treinador.id == plano_in.id_treinador)).first()
    if not t:
        raise HTTPException(status_code=404, detail="Treinador doesnt exists with this id")
          
    av = session.execute(select(Avaliacao).where(Avaliacao.id == plano_in.id_avaliacao)).first()
    if not av:
        raise HTTPException(status_code=404, detail="Avaliacao doesnt exists with this id")
    
    dietazs = session.execute(select(Dieta).where(Dieta.id == id_dieta)).first()
    if not dietazs:
        raise HTTPException(status_code=404, detail="Dieta doesnt exists with this id")
    
    
    session.add(plano)
    session.commit()
    session.refresh(plano)
    return plano

def get_max_calorias_sessao(session: SessionDep) -> Any:
    """
    Retrieve the ID of the sessao with the highest calorias_gastas_total.
    """
    sql_query = text("""
       WITH calorias_totais AS (
           SELECT 
               sessao.id AS sessao_id,
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
       )
       SELECT 
           sessao_id
       FROM 
           calorias_totais
       ORDER BY 
           calorias_gastas_total DESC
       LIMIT 1;
    """)

    result = session.execute(sql_query).fetchone()

    sessao_id = result[0] if result else None

    return sessao_id

@router.post("/planos_create_user", response_model=PlanoPublic)
def create_planos_user(
    *, session: SessionDep, current_user: CurrentUser, id_avaliacao:int,especialidade:str
) -> Any:
    """
    Create new plano.
    """

    create_procedure_sql = text("""
    CREATE OR REPLACE PROCEDURE get_dieta_by_min_calories(
        INOUT id_dieta INT
    )
    LANGUAGE plpgsql
    AS $$
    DECLARE
        calorias_limit NUMERIC := 2000;  -- Example fixed value for the calorie limit
    BEGIN
        -- Selects the id_dieta based on the calorie limit
        SELECT dr.id_dieta
        FROM dieta_refeicoes dr
        JOIN refeicao r_manha ON dr.id_ref_manha = r_manha.id
        JOIN refeicao r_tarde ON dr.id_ref_tarde = r_tarde.id
        JOIN refeicao r_noite ON dr.id_ref_noite = r_noite.id
        GROUP BY dr.id_dieta
        HAVING SUM(r_manha.calorias + r_tarde.calorias + r_noite.calorias) <= calorias_limit
        ORDER BY SUM(r_manha.calorias + r_tarde.calorias + r_noite.calorias) ASC
        LIMIT 1
        INTO id_dieta;

        IF NOT FOUND THEN
            RAISE EXCEPTION 'No diet found with the specified calories';
        END IF;
    END;
    $$;
""")

    session.execute(create_procedure_sql)
    session.commit()

    call_procedure_sql = text("CALL get_dieta_by_min_calories(:id_dieta)")
    result = session.execute(call_procedure_sql, {'id_dieta': None})

    id_dieta = result.fetchone()[0]

    
    proc = text("""
            SELECT t.id
            FROM treinador t
            WHERE t.especialidade = :especialidade
            LIMIT 1;  
        """)

    result = session.execute(proc, {'especialidade': especialidade}).fetchone()
    id_treinador = result[0] if result else None
    
    sessao_id = get_max_calorias_sessao(session=session)

    id = random.randint(0, 10000000)
    existing_plano = session.get(Plano, (id, current_user.id))
    while existing_plano:
        id = random.randint(0, 10000000)
        existing_plano = session.get(Plano,id,current_user.id)
        
    
    plano = Plano(
        id=id,
        id_user=current_user.id,
        id_sessao_treino=sessao_id,
        id_treinador=id_treinador,
        id_avaliacao=id_avaliacao,
        id_dieta=id_dieta
    )
    
    av_result = session.execute(select(Avaliacao).where(Avaliacao.id == id_avaliacao)).first()
    av = av_result[0]
    
    if not av:
        raise HTTPException(status_code=404, detail="Avaliacao doesnt exists with this id")
    elif av:
        shape_result = session.execute(
        select(Shape).where(Shape.usuario_id == current_user.id, Shape.id == av.shape_id)
    ).first()
    if not shape_result:
        raise HTTPException(status_code=404, detail="Shape photo with this user id does not exist")
    
    planez = session.get(Plano, (id, current_user.id))
    if planez:
        raise HTTPException(status_code=404, detail="Plano exists with this id")
    
      
    userz = session.execute(select(User).where(User.id == current_user.id)).first()
    if not userz:
        raise HTTPException(status_code=404, detail="there is no user with this id")
    
    sessoz = session.execute(select(Sessao).where(Sessao.id == sessao_id)).first()
    if not sessoz:
        raise HTTPException(status_code=404, detail="Sessoes doesnt exists with this id")
          
    t = session.execute(select(Treinador).where(Treinador.id == id_treinador)).first()
    if not t:
        raise HTTPException(status_code=404, detail="Treinador doesnt exists with this id")
          
    
    dietazs = session.execute(select(Dieta).where(Dieta.id == id_dieta)).first()
    if not dietazs:
        raise HTTPException(status_code=404, detail="Dieta doesnt exists with this id")
    
    
    session.add(plano)
    session.commit()
    session.refresh(plano)
    return plano




@router.put("/planos/{plano_id}", response_model=Message)
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

    if not plano:
        raise HTTPException(status_code=404, detail="Plano not found")

    if plano.id_user != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot edit a plano that is not yours")

    for key, value in plano_in.dict(exclude_unset=True).items():
        setattr(plano, key, value)

    session.commit()
    session.refresh(plano)

    return Message(message="Plano updated successfully")

def get_dieta_by_min_calorias(session: SessionDep):
    procedure_call = text("""
        SELECT id_dieta
        FROM get_dieta_by_min_calories()
    """)
    result = session.execute(procedure_call).fetchone()

    if result is None:
        raise ValueError("No dieta found with the minimum calorie limit")

    return result[0] 

@router.delete("/{id}", dependencies=[Depends(get_current_active_superuser)])
def delete_plano(
    *, session: SessionDep, id: int, current_user: CurrentUser
) -> Message:
    """
    Delete a plano.
    """
    
    plano = session.execute(select(Plano).where(Plano.id == id)).scalars().first()
    
    if plano is None:
        raise HTTPException(status_code=404, detail="Plano not found")
    
    if plano.id_user != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot delete a plano that is not yours")
    
    session.delete(plano)
    session.commit()
    
    return Message(message="Plano deleted successfully")