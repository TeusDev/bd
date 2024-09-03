import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str

# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=None, primary_key=True)
    title: str = Field(max_length=255)

# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
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
    name: str | None = Field(default=None, max_length=255)
    calorias: int | None = Field(default=None)

class Refeicao(RefeicaoBase,table=True):
    id: str = Field(default_factory=None, primary_key=True)
    
class RefeicaoCreate(RefeicaoBase):
    id: str

class RefeicaoPublic(Refeicao):
    name: str
    calorias: int

class RefeicoesPublic(SQLModel):
    data: list[RefeicaoPublic]
    count: int

class DietaBase(SQLModel):
    id_ref_manha: str | None = Field(default=None, foreign_key="refeicao.id")
    id_ref_tarde: str | None = Field(default=None, foreign_key="refeicao.id")
    id_ref_noite: str | None = Field(default=None, foreign_key="refeicao.id")

class Dieta(DietaBase,table=True):
    id: str = Field(default_factory=None, primary_key=True)

class DietaCreate(DietaBase):
    id: str


class DietaPublic(Dieta):
    id: str
    id_ref_manha: str
    id_ref_tarde: str
    id_ref_noite: str
    
class DietasPublic(SQLModel):
    data: list[DietaPublic]
    count: int

