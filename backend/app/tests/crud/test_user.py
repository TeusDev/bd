from fastapi.encoders import jsonable_encoder
from sqlmodel import Session,select
from app.core.security import get_password_hash, verify_password
from .nome_gen import choose_name

from app import crud
from app.core.security import verify_password
from app.models import User, UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string
import random

def test_create_user(db: Session) -> None:
    for i in range(10):
        email = random_email()
        password = random_lower_string()
        user_in = UserCreate(email=email, password=password)
        id = random.randint(0,10000000)
        statement = select(User).where(User.id == id)
        existing_users = db.exec(statement).first()
        if existing_users:
            continue
        
        user = User(
            id=id,
            hashed_password=get_password_hash(user_in.password),
            password=password,
            email=email,
            is_superuser=False,
            name=choose_name()
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
            
        email2 = random_email()
        password2 = random_lower_string()
        user_in2 = UserCreate(email=email2, password=password2,is_superuser=True)
        id2 = random.randint(0,10000000)

        statement2 = select(User).where(User.id == id2)
        existing_users2 = db.exec(statement2).first()
        if existing_users2:
            continue
        
        
        user2 = User(
            id=id2,
            hashed_password=get_password_hash(user_in2.password),
            password=password2,
            email=email2,
            is_superuser=True,
            name=choose_name()
        )
        
        db.add(user2)
        db.commit()
        db.refresh(user2)
        
        