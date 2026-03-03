"""
Schemas Pydantic para a entidade Materias, definindo as estruturas de dados para criação, atualização e resposta de matérias.
"""

__author__ = ["Gustavo Manganelli", "Erik Santos"]

from datetime import date
from typing import Optional
from pydantic import BaseModel
from schemas.mutantes_schema import MutanteSimpleSchema


class ObservacaoBase(BaseModel):
    observacao: str
    data: date
    mutantesmaterias_id: int


class ObservacaoCreate(ObservacaoBase):
    pass


class ObservacaoUpdate(BaseModel):
    observacao: Optional[str] = None
    data: Optional[date] = None
    mutantesmaterias_id: Optional[int] = None


class ObservacaoResponse(ObservacaoBase):
    id: Optional[int] = None


class ObservacaoSchema(BaseModel):
    id: int
    observacao: str
    data: date
    mutantesmaterias_id: int
    aluno: Optional[MutanteSimpleSchema] = None

    class Config:
        from_attributes = True


class ObservacaoStudentSchema(BaseModel):
    id: int
    observacao: str
    data: date
    materia: str
    professor: str

    class Config:
        from_attributes = True


# alias for compatibility
ObservacoesSchemas = ObservacaoSchema