import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

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
