import uuid
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
    id_dieta:     int = Field(default_factory=None, primary_key=True,foreign_key="dieta.id")
    id_ref_manha: int = Field(default_factory=None, primary_key=True,foreign_key="refeicao.id")
    id_ref_tarde: int = Field(default_factory=None, primary_key=True,foreign_key="refeicao.id")
    id_ref_noite: int = Field(default_factory=None, primary_key=True,foreign_key="refeicao.id")

class TreinadorBase(SQLModel):
    telefone: str | None = Field(max_length=11,default=None,unique=True,foreign_key= "telefone.telefone")
    name: str | None = Field(default=None, max_length=255)
    especialidade: str | None = Field(default=None, max_length=255)

# Properties to receive via API on update, all are optional
class TreinadorUpdate(TreinadorBase):
    telefone: str | None = Field(max_length=11,default=None,unique=True,foreign_key= "telefone.telefone")
    especialidade: str | None = Field(default=None, min_length=8, max_length=40)

    
class Treinador(TreinadorBase, table=True):
    id: str = Field(default=None, primary_key=True,max_length=11)

class TreinadorPublic(TreinadorBase):
    telefone: str | None = Field(max_length=11,default=None,unique=True,foreign_key= "telefone.telefone")
    name: str | None = Field(default=None, max_length=255)
    especialidade: str | None = Field(default=None, max_length=255)

class TreinadoresPublic(SQLModel):
    data: list[TreinadorPublic]
    count: int
    
class TreinadorCreate(TreinadorBase):
    id: str = Field(default=None, primary_key=True,max_length=11)
    telefone: str | None = Field(default=None, unique=True,max_length=11)
    name: str | None = Field(default=None, max_length=255)
    especialidade: str | None = Field(default=None, max_length=255)
class TelefoneBase(SQLModel):
    telefone: str = Field(default=None, primary_key=True,max_length=11)

class Telefone(TelefoneBase,table=True):
    pass

class TelefoneCreate(TelefoneBase):
    telefone: str = Field(default=None, primary_key=True,max_length=11)

# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    birthdate: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    cpf: str = Field(default=generate_cpf(),unique=True,max_length=11)
    password: str = Field(min_length=8, max_length=40)
    email: EmailStr = Field(unique=True, index=True, max_length=255)

class UserRegister(SQLModel):
    cpf: str = Field(default=generate_cpf(),unique=True,max_length=11)
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    birthdate: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    name: str | None = Field(default=None, max_length=255)


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
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    cpf: str = Field(default=generate_cpf(),unique=True,max_length=11)
    hashed_password: str

    # items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)

# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    email: str
    birthdate: datetime.datetime
    name: str


class TelefonePublic(Telefone):
    telefone: str

class TelefonesPublic(SQLModel):
    data: list[TelefonePublic]
    count: int
    
# class ItemsPublic(SQLModel):
#     data: list[ItemPublic]
#     count: int

class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# # Shared properties
# class ItemBase(SQLModel):
#     title: str = Field(min_length=1, max_length=255)
#     description: str | None = Field(default=None, max_length=255)


# # Properties to receive on item creation
# class ItemCreate(ItemBase):
#     pass


# # Properties to receive on item update
# class ItemUpdate(ItemBase):
#     title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
# class Item(ItemBase, table=True):
    # id: uuid.UUID = Field(default_factory=None, primary_key=True)
    # title: str = Field(max_length=255)
# # Database model, database table inferred from class name
# class Item(ItemBase, table=True):
#     id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
#     title: str = Field(max_length=255)
#     owner_id: uuid.UUID = Field(
#         foreign_key="user.id", nullable=False, ondelete="CASCADE"
#     )
#     owner: User | None = Relationship(back_populates="items")

# # Properties to return via API, id is always required
# class ItemPublic(ItemBase):
#     id: uuid.UUID
#     owner_id: uuid.UUID


# class ItemsPublic(SQLModel):
#     data: list[ItemPublic]
#     count: int


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

    
# Update forward references for the SQLModel
Refeicao.update_forward_refs()
    
class RefeicaoCreate(RefeicaoBase):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None, max_length=255)
    calorias: int = Field(default=None)

class RefeicaoUpdate(RefeicaoBase):
    pass

class RefeicaoPublic(RefeicaoBase):
    name: str
    calorias: int

class RefeicoesPublic(SQLModel):
    data: list[RefeicaoPublic]
    count: int

class ExercicioBase(SQLModel):
    exercicio: str = Field(default_factory=None)
    
class Exercicio(ExercicioBase, table=True):
    id: int = Field(default_factory=None, primary_key=True)

class ExercicioCreate(ExercicioBase):
    id: int = Field(default_factory=None, primary_key=True)

class ExercicioPublic(Exercicio):
    id: int
    exercicio: str
    

class ExerciciosPublic(SQLModel):
    data: list[ExercicioPublic]
    count: int
    
class TreinoBase(SQLModel):
    id_exercicio: int = Field(default=None, foreign_key="exercicio.id")
    grupo_muscular: str = Field(default=None)

class Treino(TreinoBase,table=True):
    id: int = Field(default_factory=None, primary_key=True)

class TreinoCreate(TreinoBase):
    id: int = Field(default_factory=None, primary_key=True)


class TreinoPublic(Treino):
    id: int
    id_exercicio: int
    grupo_muscular: str


class TreinosPublic(SQLModel):
    data: list[TreinoPublic]
    count: int
    

class SessaoBase(SQLModel):
    id_treino: int = Field(default=None, foreign_key="treino.id")
    data: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    duracao_minutos: int = Field(default=None)
    
class Sessao(SessaoBase,table=True):
    id: int = Field(default_factory=None, primary_key=True)

class SessaoCreate(SessaoBase):
    id: int = Field(default_factory=None, primary_key=True)


class SessaoPublic(Sessao):
    id: int
    id_treino: int
    data: datetime.datetime 
    duracao_minutos: int 
class SessoesPublic(SQLModel):
    data: list[SessaoPublic]
    count: int

class DietaBase(SQLModel):
    id: int = Field(default_factory=None, primary_key=True)

class Dieta(DietaBase,table=True):
    id: int = Field(default_factory=None, primary_key=True)

class DietaCreate(DietaBase):
    id: int
class DietaUpdate(DietaBase):
    pass


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
    id_user: uuid.UUID = Field(default_factory=uuid.uuid4, foreign_key="user.id")
    id_sessao_treino: int | None = Field(default_factory=None,foreign_key="sessao.id")
    id_treinador: str | None = Field(default_factory=None,foreign_key="treinador.id")
    id_avaliacao : int | None = Field(default_factory = None,foreign_key="avaliacao.id")

class PlanoCreate(PlanoBase):
    id_user: uuid.UUID = Field(default_factory=uuid.uuid4, foreign_key="user.id")
    id_sessao_treino: int | None = Field(default_factory=None,foreign_key="sessao.id")
    id_treinador: str | None = Field(default_factory=None,foreign_key="treinador.id")
    id_avaliacao : int | None = Field(default_factory = None,foreign_key="avaliacao.id")



class PlanoUpdate(PlanoBase):
    id_dieta: int | None = Field(default_factory=None)
    id_sessao_treino: int | None = Field(default_factory=None)
    id_treinador: str | None = Field(default_factory=None)
    id_avaliacao : int | None = Field(default_factory = None)

class Plano(PlanoBase, table=True):
    id_dieta: int | None = Field(default_factory=None,foreign_key="dieta.id")

class PlanoPublic(PlanoBase):
    pass

class PlanosPublic(SQLModel):
    data: list[PlanoPublic]
    count: int


class AvaliacaoBase(SQLModel):
    data_avaliacao: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    peso: float = Field(default = 0.0)
    altura: float = Field(default = 0.0)
    perc_gordura: float = Field(default = 0.0)
    
class AvaliacaoCreate(AvaliacaoBase):
    id: int | None = Field(default=None,primary_key=True) 


class AvaliacaoUpdate(AvaliacaoBase):
    data_avaliacao: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    peso: float = Field(default = 0.0)
    altura: float = Field(default = 0.0)
    perc_gordura: float = Field(default = 0.0)


class Avaliacao(AvaliacaoBase, table=True):
    id: int | None = Field(default=None,primary_key=True) 

class AvaliacaoPublic(AvaliacaoBase):
    id: int


class AvaliacoesPublic(SQLModel):
    data: list[AvaliacaoPublic]
    count: int
    
class ShapeBase(SQLModel):
    nome_foto: str = Field(primary_key=True)
class Shape(ShapeBase, table=True):
    foto: bytes | None = Field(default=None, sa_column=Column(LargeBinary))
class ShapeCreate(ShapeBase):
    pass
class ShapeDelete(Shape):
    pass

class ShapePublic(Shape):
    nome_foto: str
    foto: str | None = None  # Use str to store base64 encoded string

    @classmethod
    def from_orm(cls, shape):
        # Base64 encode the binary data
        foto_encoded = base64.b64encode(shape.foto).decode('utf-8') if shape.foto else None
        return cls(nome_foto=shape.nome_foto, foto=foto_encoded)

class ShapesPublic(SQLModel):
    data: list[ShapePublic]
    count: int
