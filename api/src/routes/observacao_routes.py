from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_session
from dao.observacoes_dao import ObservacoesDAO
from dao.mutantes_materias_dao import MutantesMateriasDAO
from services.observacoes_service import ObservacoesService
from schemas.observacoes_schema import ObservacaoCreate, ObservacaoUpdate, ObservacaoSchema

observacao_router = APIRouter(prefix="/observacao", tags=["observacao"])

def get_observacao_service(session: Session = Depends(get_session)) -> ObservacoesService:
    observacoes_dao = ObservacoesDAO(session)
    mutantes_materias_dao = MutantesMateriasDAO(session)
    return ObservacoesService(observacoes_dao, mutantes_materias_dao)

@observacao_router.get("/", response_model=List[ObservacaoSchema])
async def listar_todas_observacoes(service: ObservacoesService = Depends(get_observacao_service)):
    return service.listar_todas_observacoes()

@observacao_router.post("/", response_model=ObservacaoSchema, status_code=status.HTTP_201_CREATED)
async def adicionar_observacao(dados: ObservacaoCreate, service: ObservacoesService = Depends(get_observacao_service)):
    try:
        return service.adicionar_observacao(dados)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@observacao_router.get("/turma/{turma_id}", response_model=List[ObservacaoSchema])
async def listar_observacoes_por_turma(turma_id: int, service: ObservacoesService = Depends(get_observacao_service)):
    return service.listar_observacoes_por_turma(turma_id)

@observacao_router.get("/{observacao_id}", response_model=ObservacaoSchema)
async def obter_observacao(observacao_id: int, service: ObservacoesService = Depends(get_observacao_service)):
    try:
        return service.obter_observacao_por_id(observacao_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@observacao_router.patch("/{observacao_id}", response_model=ObservacaoSchema)
async def atualizar_observacao(observacao_id: int, dados: ObservacaoUpdate, service: ObservacoesService = Depends(get_observacao_service)):
    try:
        return service.atualizar_observacao(observacao_id, dados)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@observacao_router.delete("/{observacao_id}")
async def deletar_observacao(observacao_id: int, service: ObservacoesService = Depends(get_observacao_service)):
    try:
        return service.deletar_observacao(observacao_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
