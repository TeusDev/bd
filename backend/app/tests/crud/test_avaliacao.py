# from fastapi.encoders import jsonable_encoder
# from sqlmodel import Session,select
# import uuid
# from app import crud
# from app.core.security import verify_password
# from app.models import Avaliacao,AvaliacaoBase,AvaliacaoCreate,AvaliacaoPublic,AvaliacoesPublic,Shape
# from app.tests.utils.utils import random_email, random_lower_string
# import secrets
# import string
# from .nome_gen import choose_name
# import random
# from .utils import especialidades, random_datetime,start_date,end_date
# # cpf and telefone
# N=8

# def test_create_avaliacao(db: Session) -> None:
#     for i in range(20):
        
#         id = random.randint(0,10000000)
#         nome_foto=f"foto_{id}"
        
#         statement = select(Shape).where(Shape.id == id)
#         shapes = db.exec(statement).first()
#         # Caminho para a foto existente
#         existing_image_file = ".shapes/caua.png"
#         if shapes:
#             continue
        
#         with open(existing_image_file, "rb") as img_file:
#             file_contents = img_file.read()

#         shape = Shape(
#             id=id,
#             nome_foto=nome_foto,
#             foto=file_contents
#         )
        
#         db.add(shape)
#         db.commit()
#         db.refresh(shape)
        
#         data_avaliacao = random_datetime(start_date, end_date)
#         peso         = round(random.uniform(40.0, 170.0),2)
#         altura       = round(random.uniform(1.3,2.2),2)
#         perc_gordura = round(random.uniform(4.0,30.0),2)
        
#         avaliacao = AvaliacaoCreate(
#             id=id,
#             data_avaliacao = data_avaliacao,
#             peso = peso,
#             altura = altura,
#             perc_gordura = perc_gordura,
#             shape_id = id
#         )
        
#         existing_avaliacao = crud.get_avaliacoes(session=db,id=id)
#         if existing_avaliacao:
#             continue
        
#         aval = crud.create_avaliacao(session=db,avaliacao_create=avaliacao)
#         assert aval.id == id