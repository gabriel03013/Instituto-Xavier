"""
Schemas Pydantic para a entidade Materias, definindo as estruturas de dados para criação, atualização e resposta de matérias.
"""

__author__ = ["Gustavo Manganelli", "Erik Santos"]

from typing import Optional, List
from pydantic import BaseModel
from schemas.mutantes_schema import MutanteSchema


class TurmaBase(BaseModel):
    serie: int
    turma: str


class TurmaCreate(TurmaBase):
    pass


class TurmaUpdate(BaseModel):
    serie: Optional[int] = None
    turma: Optional[str] = None


class TurmaResponse(TurmaBase):
    id: Optional[int] = None


class TurmaSchema(BaseModel):
    id: int
    serie: int
    turma: str
    alunos: List[MutanteSchema] = []

    class Config:
        from_attributes = True


# compatibility alias
TurmasSchema = TurmaSchema