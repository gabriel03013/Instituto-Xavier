from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_session
from dao.mutantes_materias_dao import MutantesMateriasDAO
from dao.mutante_dao import MutanteDAO
from dao.materias_dao import MateriasDAO
from services.mutantes_materias_services import MutantesMateriasService
from schemas.mutantes_materias_schema import (
    MutantesMateriasCreate, 
    MutantesMateriasUpdate, 
    MutantesMateriasSchema,
    MutanteGradeSchema
)

mutante_materia_router = APIRouter(prefix="/mutante_materia", tags=["mutante_materia"])

def get_mutantes_materias_service(session: Session = Depends(get_session)) -> MutantesMateriasService:
    dao = MutantesMateriasDAO(session)
    mutante_dao = MutanteDAO(session)
    materias_dao = MateriasDAO(session)
    return MutantesMateriasService(dao, mutante_dao, materias_dao)

@mutante_materia_router.post("/", response_model=MutantesMateriasSchema, status_code=status.HTTP_201_CREATED)
async def matricular_mutante(dados: MutantesMateriasCreate, service: MutantesMateriasService = Depends(get_mutantes_materias_service)):
    try:
        return service.matricular_em_materia(dados)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@mutante_materia_router.get("/mutante/{mutante_id}", response_model=List[MutantesMateriasSchema])
async def listar_materias_mutante(mutante_id: int, service: MutantesMateriasService = Depends(get_mutantes_materias_service)):
    try:
        return service.listar_materias_mutante(mutante_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@mutante_materia_router.get("/materia/{materia_id}", response_model=List[MutantesMateriasSchema])
async def listar_mutantes_materia(materia_id: int, service: MutantesMateriasService = Depends(get_mutantes_materias_service)):
    try:
        return service.listar_mutantes_materia(materia_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@mutante_materia_router.patch("/{mutante_id}/{materia_id}", response_model=MutantesMateriasSchema)
async def lancar_notas(mutante_id: int, materia_id: int, dados: MutantesMateriasUpdate, service: MutantesMateriasService = Depends(get_mutantes_materias_service)):
    try:
        return service.lancar_notas(mutante_id, materia_id, dados)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@mutante_materia_router.delete("/{mutante_id}/{materia_id}")
async def remover_matricula(mutante_id: int, materia_id: int, service: MutantesMateriasService = Depends(get_mutantes_materias_service)):
    try:
        return service.remover_matricula(mutante_id, materia_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@mutante_materia_router.get("/notas/turma/{turma_id}/materia/{materia_id}", response_model=List[MutanteGradeSchema])
async def listar_notas_por_turma(turma_id: int, materia_id: int, service: MutantesMateriasService = Depends(get_mutantes_materias_service)):
    return service.listar_grades_por_turma(turma_id, materia_id)
