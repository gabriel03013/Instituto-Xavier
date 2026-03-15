"""
Schemas Pydantic para a entidade Tarefa, definindo as estruturas de dados
para criação, atualização e resposta de tarefas.
"""

__author__ = "Erik Santos"

from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class TarefaBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    status: str
    prioridade: Optional[str] = None
    data_limite: Optional[datetime] = None
    mutante_id: Optional[int] = None


class TarefaCreate(TarefaBase):
    pass


class TarefaUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[str] = None
    prioridade: Optional[str] = None
    data_limite: Optional[datetime] = None
    data_conclusao: Optional[datetime] = None


class TarefaResponse(TarefaBase):
    id: Optional[int] = None
    data_criacao: Optional[datetime] = None
    data_conclusao: Optional[datetime] = None

    class Config:
        from_attributes = True


class TarefaSchema(BaseModel):
    id: int
    titulo: str
    status: str
    prioridade: Optional[str] = None
    data_limite: Optional[datetime] = None

    class Config:
        from_attributes = True