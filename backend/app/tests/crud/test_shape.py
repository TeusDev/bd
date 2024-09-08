from fastapi.encoders import jsonable_encoder
from sqlmodel import Session,select
import uuid
from app import crud
from app.core.security import verify_password
from app.models import Avaliacao,AvaliacaoBase,AvaliacaoCreate,AvaliacaoPublic,AvaliacoesPublic,Shape,ShapeCreate
from app.tests.utils.utils import random_email, random_lower_string
import secrets
import string
from .nome_gen import choose_name
import random
from .utils import especialidades, random_datetime,start_date,end_date
# cpf and telefone
N = 11

def test_create_shape(db: Session) -> None:
    for i in range(20):
     
        id = random.randint(0,10000000)
        nome_foto=f"foto_{id}"
        
        statement = select(Shape).where(Shape.id == id)
        shapes = db.exec(statement).first()
        # Caminho para a foto existente
        existing_image_file = "shapes/caua.png"
        if shapes:
            continue
        
        with open(existing_image_file, "rb") as img_file:
            file_contents = img_file.read()

        shape = Shape(
            id=id,
            nome_foto=nome_foto,
            foto=file_contents
        )
        
        db.add(shape)
        db.commit()
        db.refresh(shape)