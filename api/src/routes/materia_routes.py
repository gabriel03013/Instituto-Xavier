from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_session
from dao.materias_dao import MateriasDAO
from services.materia_service import MateriaService
from schemas.materias_schema import MateriaCreate, MateriaUpdate, MateriaSchema

materia_router = APIRouter(prefix="/materia", tags=["materia"])

def get_materia_service(session: Session = Depends(get_session)) -> MateriaService:
    materias_dao = MateriasDAO(session)
    return MateriaService(materias_dao)

@materia_router.get("/", response_model=List[MateriaSchema])
async def listar_materias(service: MateriaService = Depends(get_materia_service)):
    return service.listar_materias()

@materia_router.post("/", response_model=MateriaSchema, status_code=status.HTTP_201_CREATED)
async def criar_materia(dados: MateriaCreate, service: MateriaService = Depends(get_materia_service)):
    return service.criar_novo_materia(dados)

@materia_router.patch("/{materia_id}", response_model=MateriaSchema)
async def atualizar_materia(materia_id: int, dados: MateriaUpdate, service: MateriaService = Depends(get_materia_service)):
    try:
        return service.atualizar_materia(materia_id, dados)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@materia_router.delete("/{materia_id}")
async def deletar_materia(materia_id: int, service: MateriaService = Depends(get_materia_service)):
    try:
        return service.deletar_materia(materia_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
