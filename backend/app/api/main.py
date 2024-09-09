from fastapi import APIRouter


from app.api.routes import (
    login,
    refeicao,
    dieta,
    users, 
    utils, 
    treinadores,
    planos,
    avaliacoes,
    shapes,
    sessoes,
    treinos,
    exercicios,
    locais
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(refeicao.router, prefix="/refeicoes", tags=["refeicoes"])
api_router.include_router(dieta.router, prefix="/dietas", tags=["dietas"])
api_router.include_router(locais.router,prefix="/locais",tags=["locais"])
api_router.include_router(treinadores.router,prefix="/treinadores",tags=["treinadores"])
api_router.include_router(planos.router,prefix="/planos",tags=["planos"])
api_router.include_router(avaliacoes.router,prefix="/avaliacoes",tags=["avaliacoes"])
api_router.include_router(shapes.router,prefix="/shapes,",tags=["shapes"])
api_router.include_router(sessoes.router,prefix="/sessoes,",tags=["sessoes"])
api_router.include_router(treinos.router,prefix="/treinos,",tags=["treinos"])
api_router.include_router(exercicios.router,prefix="/exercicios,",tags=["exercicios"])

