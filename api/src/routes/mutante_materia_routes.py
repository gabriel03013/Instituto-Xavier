"""
Rotas que gerenciam as matrículas dos mutantes em matérias e também o
lançamento de notas. Inclui endpoints para listar registros por mutante,
por matéria, lançar notas, remover matrícula e consultar notas por turma
e matéria.
"""

__author__ = ["Gustavo Manganelli", "Erik Santos", "Gabriel Mendes"]

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
    """
    Cria instância do serviço de relacionamento mutante_matéria.
    
    Args:
        session (Session): Conexão do banco de dados injetada pela dependência.
    
    Returns:
        MutantesMateriasService: Instância do serviço de relacionamento mutante_matéria.
    """
    dao = MutantesMateriasDAO(session)
    mutante_dao = MutanteDAO(session)
    materias_dao = MateriasDAO(session)
    return MutantesMateriasService(dao, mutante_dao, materias_dao)

@mutante_materia_router.post("/", response_model=MutantesMateriasSchema, status_code=status.HTTP_201_CREATED)
async def matricular_mutante(dados: MutantesMateriasCreate, service: MutantesMateriasService = Depends(get_mutantes_materias_service)):
    """
    Cria um registro de matrícula de mutante

    Args:
        dados (MutantesMateriasCreate): Schema de create
        service (MutantesMateriasService, optional): Service para lógica e validação. Defaults to Depends(get_mutantes_materias_service).

    Raises:
        HTTPException: Caso haja captação de erro validação 

    Returns:
        MutantesMateriasSchema: Registro de matrícula criado.
    """
    
    try:
        return service.matricular_em_materia(dados)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@mutante_materia_router.get("/mutante/{mutante_id}", response_model=List[MutantesMateriasSchema])
async def listar_materias_mutante(mutante_id: int, service: MutantesMateriasService = Depends(get_mutantes_materias_service)):
    """
    Lista todas as matérias em que um mutante específico está matriculado.
    
    Args:
        mutante_id (int): ID do mutante para o qual buscar as matérias.
        service (MutantesMateriasService, optional): Service para lógica e validação. Defaults to Depends(get_mutantes_materias_service).
    
    Raises:
        HTTPException: Caso o mutante não seja encontrado.
    
    Returns:
        List[MutantesMateriasSchema]: Lista de registros de matrícula do mutante.
    """
    try:
        return service.listar_materias_mutante(mutante_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@mutante_materia_router.get("/materia/{materia_id}", response_model=List[MutantesMateriasSchema])
async def listar_mutantes_materia(materia_id: int, service: MutantesMateriasService = Depends(get_mutantes_materias_service)):
    """
    Lista todos os mutantes matriculados em uma matéria específica.
    
    Args:
        materia_id (int): ID da matéria para a qual buscar os mutantes.
        service (MutantesMateriasService, optional): Service para lógica e validação. Defaults to Depends(get_mutantes_materias_service).
    
    Raises:
        HTTPException: Caso a matéria não seja encontrada.
    
    Returns:
        List[MutantesMateriasSchema]: Lista de registros de matrícula da matéria.
    """
    try:
        return service.listar_mutantes_materia(materia_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@mutante_materia_router.patch("/{mutante_id}/{materia_id}", response_model=MutantesMateriasSchema)
async def lancar_notas(mutante_id: int, materia_id: int, dados: MutantesMateriasUpdate, service: MutantesMateriasService = Depends(get_mutantes_materias_service)):
    """
    Lança ou atualiza as notas de um mutante em uma matéria específica.
    
    Args:
        mutante_id (int): ID do mutante.
        materia_id (int): ID da matéria.
        dados (MutantesMateriasUpdate): Schema com os dados de notas a serem atualizados.
        service (MutantesMateriasService, optional): Service para lógica e validação. Defaults to Depends(get_mutantes_materias_service).
    
    Raises:
        HTTPException: Caso haja erro na validação dos dados.
    
    Returns:
        MutantesMateriasSchema: Registro de matrícula atualizado com as notas.
    """
    try:
        return service.lancar_notas(mutante_id, materia_id, dados)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@mutante_materia_router.delete("/{mutante_id}/{materia_id}")
async def remover_matricula(mutante_id: int, materia_id: int, service: MutantesMateriasService = Depends(get_mutantes_materias_service)):
    """
    Remove a matrícula de um mutante em uma matéria específica.
    
    Args:
        mutante_id (int): ID do mutante.
        materia_id (int): ID da matéria.
        service (MutantesMateriasService, optional): Service para lógica e validação. Defaults to Depends(get_mutantes_materias_service).
    
    Raises:
        HTTPException: Caso a matrícula não seja encontrada.
    
    Returns:
        dict: Confirmação da remoção da matrícula.
    """
    try:
        return service.remover_matricula(mutante_id, materia_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@mutante_materia_router.get("/notas/turma/{turma_id}/materia/{materia_id}", response_model=List[MutanteGradeSchema])
async def listar_notas_por_turma(turma_id: int, materia_id: int, service: MutantesMateriasService = Depends(get_mutantes_materias_service)):
    """
    Lista todas as notas dos mutantes de uma turma específica em uma matéria.
    
    Args:
        turma_id (int): ID da turma.
        materia_id (int): ID da matéria.
        service (MutantesMateriasService, optional): Service para lógica e validação. Defaults to Depends(get_mutantes_materias_service).
    
    Returns:
        List[MutanteGradeSchema]: Lista de mutantes com suas notas na matéria.
    """
    return service.listar_grades_por_turma(turma_id, materia_id)

@mutante_materia_router.post("/materia/{materia_id}/lancar_quiz/{quiz_id}")
async def lancar_quiz(materia_id: int, quiz_id: int, service: MutantesMateriasService = Depends(get_mutantes_materias_service)):
    try:
        return service.lancar_quiz(materia_id, quiz_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
