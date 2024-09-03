from fastapi import APIRouter

from app.api.routes import (
    login, 
    users, 
    utils, 
    telefones,
    treinadores,
    planos,
    avaliacoes
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(telefones.router,prefix="/telefones",tags=["telefones"])
api_router.include_router(treinadores.router,prefix="/treinadores",tags=["treinadores"])
api_router.include_router(planos.router,prefix="/planos",tags=["planos"])
api_router.include_router(avaliacoes.router,prefix="/avaliacoes",tags=["avaliacoes"])


# api_router.include_router(items.router, prefix="/items", tags=["items"])
