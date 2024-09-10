from decimal import Decimal
from pydantic import EmailStr,BaseModel
from sqlmodel import Field, Relationship, SQLModel,Session,create_engine,select
import datetime
from .cpf import generate_cpf
from sqlalchemy import LargeBinary
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import base64
from typing import TYPE_CHECKING, Optional,List


class dieta_refeicoes(SQLModel,table=True):
    id_dieta:     int = Field(default_factory=None, primary_key=True,foreign_key="dieta.id", ondelete="CASCADE")
    id_ref_manha: int = Field(default_factory=None, primary_key=True,foreign_key="refeicao.id", ondelete="CASCADE")
    id_ref_tarde: int = Field(default_factory=None, primary_key=True,foreign_key="refeicao.id", ondelete="CASCADE")
    id_ref_noite: int = Field(default_factory=None, primary_key=True,foreign_key="refeicao.id", ondelete="CASCADE")

class TreinadorBase(SQLModel):
    telefone: str | None = Field(max_length=11,default=None,unique=True)
    name: str | None = Field(default=None, max_length=255)
    especialidade: str | None = Field(default=None, max_length=255)

# Properties to receive via API on update, all are optional
class TreinadorUpdate(TreinadorBase):
    telefone: str | None = Field(max_length=8,default=None,unique=True)
    especialidade: str | None = Field(default=None, min_length=8, max_length=40)

    
class Treinador(TreinadorBase, table=True):
    id: str = Field(default=None, primary_key=True,max_length=11)

class TreinadorPublic(SQLModel):
    id: Optional[str]
    name: Optional[str] 
    telefone: Optional[str]
    especialidade: Optional[str]
    telefone: Optional[str]
    local_de_treino: Optional[str]
class TreinadoresPublic(SQLModel):
    data: list[TreinadorPublic]
    count: int
    
class TreinadorCreate(SQLModel):
    id: str = Field(default=None, primary_key=True,max_length=11)
    name: str | None = Field(default=None, max_length=255)
    especialidade: str | None = Field(default=None, max_length=255)
    telefone: str | None = Field(max_length=8,default=None,unique=True)
class LocalBase(SQLModel):
    nome_local: str = Field(default=None, max_length=255)
    
class Local(LocalBase,table=True):
    id: int = Field(default=None, primary_key=True)

class treinador_locais(SQLModel,table=True):
    treinador_id: str = Field(default=None, primary_key=True,max_length=11,foreign_key="treinador.id", ondelete="CASCADE")
    local_id: int = Field(default=None, primary_key=True,foreign_key="local.id", ondelete="CASCADE")
    

class LocalPublic(Local):
    pass
class LocaisPublic(SQLModel):
    data: list[LocalPublic]
    count: int
    
class LocalCreate(LocalBase):
    id: int = Field(default=None, primary_key=True)

# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    name: str | None = Field(default=None, max_length=255)
    id: Optional[int] = Field(default=None, primary_key=True)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

    # items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)

# Properties to return via API, id is always required
class UserPublic(UserBase):
    email: str
    id: int
    name:str | None

class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int

# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)

##########LUCAS###########################

class RefeicaoBase(SQLModel):
    name: str = Field(default=None, max_length=255)
    calorias: int = Field(default=None)


class Refeicao(RefeicaoBase, table=True):
    id: int = Field(default=None, primary_key=True)

    
class RefeicaoCreate(RefeicaoBase):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None, max_length=255)
    calorias: int = Field(default=None)

class RefeicaoUpdate(RefeicaoBase):
    pass

class RefeicaoPublic(RefeicaoBase):
    id: int
    name: str
    calorias: int

class RefeicoesPublic(SQLModel):
    data: list[RefeicaoPublic]
    count: int

class ExercicioBase(SQLModel):
    exercicio: str = Field(default_factory=None)
    grupo_muscular: str | None = Field(default=None)
class Exercicio(ExercicioBase, table=True):
    id: int = Field(default_factory=None, primary_key=True)

class ExercicioCreate(SQLModel):
    id: int = Field(default_factory=None, primary_key=True)
    exercicio: str = Field(default_factory=None)
    grupo_muscular: str | None = Field(default=None)
class ExercicioPublic(Exercicio):
    id: int
    exercicio: str
    grupo_muscular: str 
    
class ExercicioQueryPublic(SQLModel):
    id: int
    exercicio: str
    grupo_muscular: str 


class ExerciciosQueryPublic(SQLModel):
    data: list[ExercicioQueryPublic]
    count: int


class ExerciciosPublic(SQLModel):
    data: list[ExercicioPublic]
    count: int
    
class TreinoBase(SQLModel):
    calorias: int = Field(default=None)
    

class Treino(TreinoBase,table=True):
    id: int = Field(default_factory=None, primary_key=True)

class TreinoCreate(TreinoBase):
    id: int = Field(default_factory=None, primary_key=True)


class TreinoPublic(SQLModel):
    id: int
    id_exercicio: int
    calorias: int

class TreinosPublic(SQLModel):
    data: list[TreinoPublic]
    count: int
    
class treino_exercicio(SQLModel,table=True):
    id_treino: int = Field(default=None, foreign_key="treino.id",primary_key=True, ondelete="CASCADE")
    id_exercicio: int = Field(default=None, foreign_key="exercicio.id",primary_key=True, ondelete="CASCADE")

class SessaoBase(SQLModel):
    data: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    duracao_minutos: int = Field(default=None)
    
class Sessao(SessaoBase,table=True):
    id: int = Field(default_factory=None, primary_key=True)

class SessaoCreate(SessaoBase):
    id: int = Field(default_factory=None, primary_key=True)
    data: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    duracao_minutos: int = Field(default=None)


class SessaoPublic(SQLModel):
    id: int
    data: datetime.datetime 
    duracao_total: int
    exercicio1: str
    exercicio2: str
    exercicio3: str
    grupo_muscular1: str
    grupo_muscular2: str
    grupo_muscular3: str
    calorias_gastas: int
    
    
class SessoesPublic(SQLModel):
    data: list[SessaoPublic]
    count: int

class treino_sessao(SQLModel,table=True):
    id_treino1: int = Field(default=None, foreign_key="treino.id",primary_key=True, ondelete="CASCADE")
    id_treino2: int = Field(default=None, foreign_key="treino.id",primary_key=True, ondelete="CASCADE")
    id_treino3: int = Field(default=None, foreign_key="treino.id",primary_key=True, ondelete="CASCADE")
    id_sessao: int = Field(default=None, foreign_key="sessao.id",primary_key=True , ondelete="CASCADE")

class DietaBase(SQLModel):
    id: int = Field(default_factory=None, primary_key=True)

class Dieta(DietaBase,table=True):
    id: int = Field(default_factory=None, primary_key=True)

class DietaCreate(DietaBase):
    id: int
class DietaUpdate(SQLModel):
    id_ref_manha: Optional[int]
    id_ref_tarde: Optional[int]
    id_ref_noite: Optional[int]

class Plan(SQLModel):
    plano_id: int
    usuarios_id: int
    user_name: str
    sessao_duracao_minutos: int
    sessao_data: Optional[datetime.datetime]
    treinador_name: Optional[str] 
    treinador_telefone: Optional[str] 
    treinador_especialidade: Optional[str] 
    avaliacao_peso: Optional[float] 
    avaliacao_altura: Optional[float]
    avaliacao_perc_gordura: Optional[float] 
    avaliacao_shape_id: Optional[int] 
    
class viewPlano(SQLModel):
    data: list[Plan]

class DietaPublic(SQLModel):
    id: Optional[int]
    nome_ref_manha: Optional[str]
    nome_ref_tarde: Optional[str]
    nome_ref_noite: Optional[str]
    
class DietasPublic(SQLModel):
    data: list[DietaPublic]
    count: int

class PlanoBase(SQLModel):
    id: int | None = Field(default_factory=None, primary_key=True)
    id_user: int = Field(default_factory=None, primary_key=True,foreign_key="user.id", ondelete="CASCADE")
    id_sessao_treino: int | None = Field(default_factory=None,foreign_key="sessao.id", ondelete="CASCADE")
    id_treinador: str | None = Field(default_factory=None,foreign_key="treinador.id", ondelete="CASCADE")
    id_avaliacao : int | None = Field(default_factory = None,foreign_key="avaliacao.id", ondelete="CASCADE")
    
class PlanoCreate(PlanoBase):
    # id_user: int = Field(default_factory=None, foreign_key="user.id")
    id_sessao_treino: int | None = Field(default_factory=None,foreign_key="sessao.id", ondelete="CASCADE")
    id_treinador: str | None = Field(default_factory=None,foreign_key="treinador.id", ondelete="CASCADE")
    id_avaliacao : int | None = Field(default_factory = None,foreign_key="avaliacao.id", ondelete="CASCADE")



class PlanoUpdate(SQLModel):
    id_dieta: int | None = Field(default_factory=None)
    id_sessao_treino: int | None = Field(default_factory=None)
    id_treinador: str | None = Field(default_factory=None)
    id_avaliacao : int | None = Field(default_factory = None)

class Plano(PlanoBase, table=True):
    id_dieta: int | None = Field(default_factory=None,foreign_key="dieta.id", ondelete="CASCADE")

class PlanoPublic(PlanoBase):
    id_dieta: Optional[int] 


class PlanosPublic(SQLModel):
    data: list[PlanoPublic]
    count: int


class AvaliacaoBase(SQLModel):
    data_avaliacao: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    peso: float = Field(default = 0.0)
    altura: float = Field(default = 0.0)
    perc_gordura: float = Field(default = 0.0)
    shape_id: int | None = Field(default=None,foreign_key="shape.id", ondelete="CASCADE") 
    
class AvaliacaoCreate(AvaliacaoBase):
    id: int | None = Field(default=None,primary_key=True) 


class AvaliacaoUpdate(AvaliacaoBase):
    data_avaliacao: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    peso: float = Field(default = 0.0)
    altura: float = Field(default = 0.0)
    perc_gordura: float = Field(default = 0.0)




class AvaliacaoPublic(AvaliacaoBase):
    id: int


class AvaliacoesPublic(SQLModel):
    data: list[AvaliacaoPublic]
    count: int
    
class ShapeBase(SQLModel):
    nome_foto: str = Field(default=None)
    usuario_id: int | None = Field(default=None, foreign_key="user.id", ondelete="CASCADE")
class Shape(ShapeBase, table=True):
    id: int | None = Field(default=None,primary_key=True) 
    foto: bytes | None = Field(default=None, sa_column=Column(LargeBinary))
class ShapeCreate(Shape):
    pass
class ShapeDelete(Shape):
    pass

class ShapePublic(SQLModel):
    id: int
    nome_foto: str
    foto: str | None = None  # Use str to store base64 encoded string
    usuario_id: int
    @classmethod
    def from_orm(cls, shape):
        # Base64 encode the binary data
        foto_encoded = base64.b64encode(shape.foto).decode('utf-8') if shape.foto else None
        return cls(id=shape.id,nome_foto=shape.nome_foto,usuario_id=shape.usuario_id, foto=foto_encoded)

class ShapesPublic(SQLModel):
    data: list[ShapePublic]
    count: int
    
class Avaliacao(AvaliacaoBase, table=True):
    id: int | None = Field(default=None,primary_key=True)