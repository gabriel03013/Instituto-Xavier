"""
Rotas para o recurso de turma, fornecendo endpoints para listar, criar, obter,
atualizar e excluir turmas. Também permite filtrar turmas por série.
"""

__author__ = ["Gabriel Mendes", "Erik Santos"]

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_session
from dao.turmas_dao import TurmasDAO
from dao.mutante_dao import MutanteDAO
from services.turmas_service import TurmasService
from schemas.turmas_schema import TurmaCreate, TurmaUpdate, TurmaSchema

turma_router = APIRouter(prefix="/turma", tags=["turma"])

def get_turmas_service(session: Session = Depends(get_session)) -> TurmasService:
    turmas_dao = TurmasDAO(session)
    mutante_dao = MutanteDAO(session)
    return TurmasService(turmas_dao, mutante_dao)

@turma_router.get("/", response_model=List[TurmaSchema])
async def listar_turmas(service: TurmasService = Depends(get_turmas_service)):
    """
    Lista todas as turmas cadastradas.

    Args:
        service (TurmasService, optional): Serviço de turmas.
            Defaults to Depends(get_turmas_service).

    Returns:
        List[TurmaSchema]: Lista de turmas cadastradas no sistema.
    """
    return service.listar_turmas()

@turma_router.post("/", response_model=TurmaSchema, status_code=status.HTTP_201_CREATED)
async def criar_turma(dados: TurmaCreate, service: TurmasService = Depends(get_turmas_service)):
    """
    Cria uma nova turma.

    Args:
        dados (TurmaCreate): Dados da turma a ser criada.
        service (TurmasService, optional): Serviço de turmas.
            Defaults to Depends(get_turmas_service).

    Returns:
        TurmaSchema: Turma criada no sistema.
    """
    try:
        return service.criar_nova_turma(dados)
    except ValueError as e:
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@turma_router.get("/{turma_id}", response_model=TurmaSchema)
async def obter_turma(turma_id: int, service: TurmasService = Depends(get_turmas_service)):
    """
    Obtém os detalhes de uma turma específica pelo ID.

    Args:
        turma_id (int): ID da turma.
        service (TurmasService, optional): Serviço de turmas.
            Defaults to Depends(get_turmas_service).

    Raises:
        HTTPException: 404 se a turma não for encontrada.

    Returns:
        TurmaSchema: Dados da turma.
    """
    try:
        return service.obter_turma_por_id(turma_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@turma_router.get("/serie/{serie}", response_model=List[TurmaSchema])
async def listar_turmas_por_serie(serie: int, service: TurmasService = Depends(get_turmas_service)):
    """
    Lista turmas filtrando pela série.

    Args:
        serie (int): Série de interesse.
        service (TurmasService, optional): Serviço de turmas.
            Defaults to Depends(get_turmas_service).

    Returns:
        List[TurmaSchema]: Turmas que pertencem à série especificada.
    """
    return service.listar_turmas_por_serie(serie)

@turma_router.patch("/{turma_id}", response_model=TurmaSchema)
async def atualizar_turma(turma_id: int, dados: TurmaUpdate, service: TurmasService = Depends(get_turmas_service)):
    """
    Atualiza os dados de uma turma existente.

    Args:
        turma_id (int): ID da turma a ser atualizada.
        dados (TurmaUpdate): Dados novos.
        service (TurmasService, optional): Serviço de turmas.
            Defaults to Depends(get_turmas_service).

    Returns:
        TurmaSchema: Turma atualizada.
    """
    try:
        return service.atualizar_turma(turma_id, dados)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@turma_router.delete("/{turma_id}")
async def deletar_turma(turma_id: int, service: TurmasService = Depends(get_turmas_service)):
    """
    Remove uma turma do sistema.

    Args:
        turma_id (int): ID da turma a ser deletada.
        service (TurmasService, optional): Serviço de turmas.
            Defaults to Depends(get_turmas_service).

    Raises:
        HTTPException: 404 se a turma não existir.

    Returns:
        dict: Mensagem de confirmação de exclusão.
    """
    try:
        return service.deletar_turma(turma_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
