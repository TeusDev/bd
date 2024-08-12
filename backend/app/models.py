import uuid
from decimal import Decimal
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel,Session,create_engine,select
import datetime

class Plano(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    id_user: int | None = Field(default=None, foreign_key="user.id")
    id_dieta: int | None = Field(default=None, foreign_key="dieta.id")
    id_sessao_treino: int | None = Field(default=None, foreign_key="sessao_treino.id")
    id_treinador: int | None = Field(default=None, foreign_key="treinador.id")
    id_avaliacao: int | None = Field(default=None, foreign_key="avaliacao.id")
    id_local: int | None = Field(default=None, foreign_key="local.id")

class Avaliacoes(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    data_avaliacao: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
    )
    peso: Decimal = Field(default=0, max_digits=5, decimal_places=2)
    altura: Decimal = Field(default=0, max_digits=5, decimal_places=2)
    perc_gordura: Decimal = Field(default=0, max_digits=5, decimal_places=2)

class Dieta(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    id_ref_manha: int | None = Field(default=None, primary_key=True,foreign_key="refeicao.id")
    id_ref_tarde: int | None = Field(default=None, primary_key=True,foreign_key="refeicao.id")
    id_ref_noite: int | None = Field(default=None, primary_key=True,foreign_key="refeicao.id")

class Sessao_treino(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    id_treino: int | None = Field(default=None, primary_key=True,foreign_key="treino.id")
    data: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow,
    )
    duracao_minutos: int | None = Field(default=None)


class Treino(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    id_exercicio: int | None = Field(default=None, primary_key=True,foreign_key="exercicio.id")
    grupo_muscular:str | None = Field(default=None, max_length=255)

class Exercicio(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    exercicio:str | None = Field(default=None, max_length=255)
class Refeicao(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None, max_length=255)
    calorias: int | None = Field(default=None)
class Local(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None, max_length=255,primary_key=True)

class Treinador(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    id_telefone: int | None = Field(default=None, primary_key=True,foreign_key= "telefone.id")
    name: str | None = Field(default=None, max_length=255)
    especialidade: str | None = Field(default=None, max_length=255)

class Telefone(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    telefone: str | None = Field(default=None, max_length=255,primary_key=True)
    
# Shared properties
class User(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(User):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(User):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(User, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str


# Properties to return via API, id is always required
class UserPublic(User):
    id: uuid.UUID


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
