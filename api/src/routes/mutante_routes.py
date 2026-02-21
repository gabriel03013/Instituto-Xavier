from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from dao.mutante_dao import MutanteDAO
from dao.mutantes_materias_dao import MutantesMateriasDAO
from dao.poder_dao import PoderDAO
from dao.turmas_dao import TurmasDAO
from schemas.mutantes_schema import MutanteBase, MutanteCreate
from dependencies import get_session
from database import engine
from dependencies import get_session
from models import Mutante
from db.helpers.security import hash_password
from services.mutante_service import MutanteService
from dao.boletim_dao import BoletimDAO


mutante_router = APIRouter(prefix="/mutant", tags=["mutant"])


def get_mutante_service(session: Session = Depends(get_session)) -> MutanteService:
    return MutanteService(
        mutante_dao=MutanteDAO(session),
        poder_dao=PoderDAO(session),
        turmas_dao=TurmasDAO(session),
        mutantes_materias_dao=MutantesMateriasDAO(session)
    )

@mutante_router.get("/")
async def home():
    return {"msg": "Welcome, mutant!"}


# -- CREATE --
@mutante_router.post("/register_mutante")
async def register_mutante(
    mutante_schema: MutanteCreate,
    session: Session = Depends(get_session),
    service: MutanteService = Depends(get_mutante_service)
):
    """
    Mutante recebe numero da matricula por fora e backend valida se existe ou nao. admin ja inseriu a matricula no banco
    """
    new_mutante = service.registrar_novo_mutante(mutante_schema)

    return {"msg": f"New Mutante inserted successfuly! ID: {new_mutante.id}"}


# -- READ --
@mutante_router.get("/list")
async def list_mutantes(
    service: MutanteService = Depends(get_mutante_service)
):
    mutantes = service.listar_mutantes()

    if not mutantes:
        raise HTTPException(status_code=404, detail="Couldn't find any mutante")

    return {"mutantes": mutantes}


@mutante_router.get("/find_mutante")
async def find_mutante(
    id: int,
    service: MutanteService = Depends(get_mutante_service)
):
    
    return {"mutante": "mutante"}


@mutante_router.put("/complete_registration")
async def complete_registration(
    mutante_schema: MutanteCreate,
    service: MutanteService = Depends(get_mutante_service)
):
    """
    Mutante recebe número da matrícula por fora e back-end verifica se a matrícula existe e pode ser usada, atualizando o registro com os dados enviados nessa requisição.
    """
    try:
        service.completar_cadastro(mutante_schema)

        return {"msg": "Registration completed successfully."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@mutante_router.get("/my_grades")
async def see_my_grades(
    id_mutante: int,
    session: Session = Depends(get_session)
):
    boletim_dao = BoletimDAO(session)
    boletim = boletim_dao.obter_minhas_notas(id_mutante)

    if not boletim:
        raise HTTPException(status_code=404, detail="Grades are not avaiable.")
    
    return {"grades": boletim}