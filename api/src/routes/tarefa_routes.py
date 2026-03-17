"""
Rotas relacionadas às tarefas criadas pelos mutantes. Permite criar,
listar, editar, deletar e filtrar tarefas por status.
"""

__author__ = "Erik Santos"

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from dependencies import get_session
from dao.tarefa_dao import TarefaDAO
from services.tarefa_service import TarefaService
from schemas.tarefas_schema import (
    TarefaCreate,
    TarefaUpdate,
    TarefaSchema,
    TarefaResponse
)

tarefa_router = APIRouter(prefix="/tarefa", tags=["tarefa"])


def get_tarefa_service(session: Session = Depends(get_session)) -> TarefaService:
    """
    Cria instância do serviço de tarefas.

    Args:
        session (Session): Sessão do banco de dados.

    Returns:
        TarefaService: Instância do serviço de tarefas.
    """
    return TarefaService(
        tarefa_dao=TarefaDAO(session)
    )


@tarefa_router.post("/create", response_model=TarefaResponse)
async def criar_tarefa(
    dados: TarefaCreate,
    service: TarefaService = Depends(get_tarefa_service)
):
    """
    Cria uma nova tarefa.

    Args:
        dados (TarefaCreate): Dados da tarefa.
        service (TarefaService): Serviço responsável pela lógica da tarefa.

    Returns:
        TarefaResponse: Tarefa criada.
    """
    return service.criar_tarefa(dados)


@tarefa_router.get("/list", response_model=List[TarefaSchema])
async def listar_tarefas(
    service: TarefaService = Depends(get_tarefa_service)
):
    """
    Lista todas as tarefas cadastradas.

    Args:
        service (TarefaService): Serviço de tarefas.

    Raises:
        HTTPException: Caso nenhuma tarefa seja encontrada.

    Returns:
        List[TarefaSchema]: Lista de tarefas.
    """
    tarefas = service.listar_tarefas()

    if not tarefas:
        raise HTTPException(status_code=404, detail="Nenhuma tarefa encontrada.")

    return tarefas


@tarefa_router.get("/mutante/{mutante_id}", response_model=List[TarefaSchema])
async def listar_tarefas_por_mutante(
    mutante_id: int,
    service: TarefaService = Depends(get_tarefa_service)
):
    """
    Recupera todas as tarefas associadas a um mutante específico.

    Args:
        mutante_id (int): ID do mutante.
        service (TarefasService, optional): Serviço de tarefas.

    Returns:
        List[TarefaSchema]: Lista de tarefas encontradas.
    """
    return service.listar_tarefas_por_mutante(mutante_id)


@tarefa_router.get("/status/{status}", response_model=List[TarefaSchema])
async def listar_por_status(
    status: str,
    service: TarefaService = Depends(get_tarefa_service)
):
    """
    Lista todas as tarefas filtradas pelo status.

    Args:
        status (str): Status da tarefa (Pendente, Em andamento, Cancelada, Concluída).
        service (TarefaService): Serviço responsável pela lógica das tarefas.

    Raises:
        HTTPException: Caso nenhuma tarefa seja encontrada.

    Returns:
        List[TarefaSchema]: Lista de tarefas com o status informado.
    """
    tarefas = service.listar_tarefas_por_status(status)

    if not tarefas:
        raise HTTPException(status_code=404, detail="Nenhuma tarefa encontrada com esse status.")

    return tarefas


@tarefa_router.patch("/{tarefa_id}", response_model=TarefaSchema)
async def editar_tarefa(
    tarefa_id: int,
    dados: TarefaUpdate,
    service: TarefaService = Depends(get_tarefa_service)
):
    """
    Atualiza uma tarefa existente.

    Args:
        tarefa_id (int): ID da tarefa.
        dados (TarefaUpdate): Dados atualizados.
        service (TarefaService): Serviço de tarefas.

    Raises:
        HTTPException: Caso a tarefa não seja encontrada.

    Returns:
        TarefaSchema: Tarefa atualizada.
    """
    try:
        return service.atualizar_tarefa(tarefa_id, dados)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@tarefa_router.delete("/{tarefa_id}")
async def deletar_tarefa(
    tarefa_id: int,
    service: TarefaService = Depends(get_tarefa_service)
):
    """
    Deleta uma tarefa do sistema.

    Args:
        tarefa_id (int): ID da tarefa.
        service (TarefaService): Serviço de tarefas.

    Raises:
        HTTPException: Caso a tarefa não exista.

    Returns:
        dict: Confirmação da exclusão.
    """
    try:
        return service.deletar_tarefa(tarefa_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@tarefa_router.patch("/{tarefa_id}/concluir", response_model=TarefaSchema)
async def concluir_tarefa(
    tarefa_id: int,
    service: TarefaService = Depends(get_tarefa_service)
):
    """
    Marca uma tarefa como concluída.

    Args:
        tarefa_id (int): ID da tarefa a ser concluída.
        service (TarefasService, optional): Serviço de tarefas.
            Defaults to Depends(get_tarefa_service).

    Raises:
        HTTPException: 404 se a tarefa não for encontrada.

    Returns:
        TarefaSchema: Tarefa atualizada com status de concluída.
    """
    try:
        return service.concluir_tarefa(tarefa_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
