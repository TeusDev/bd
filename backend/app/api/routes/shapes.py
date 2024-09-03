import uuid
from typing import Any

from fastapi import (
    APIRouter, 
    HTTPException,
    UploadFile,
    File
)
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Plano,
    PlanoBase,
    PlanoCreate,
    PlanosPublic,
    PlanoUpdate,
    PlanoPublic
)

router = APIRouter()

@router.post("/shapes/")
async def create_upload_file(file: UploadFile = File(...)):

    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()  # <-- Important!

    # example of how you can save the file
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)

    return {"filename": file.filename}


@router.get("/shapes/")
async def read_random_file():

    # get a random file from the image directory
    files = os.listdir(IMAGEDIR)
    random_index = randint(0, len(files) - 1)

    path = f"{IMAGEDIR}{files[random_index]}"
    
    # notice you can use FileResponse now because it expects a path
    return FileResponse(path)
