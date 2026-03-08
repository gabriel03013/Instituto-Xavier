"""
Schemas Pydantic para a entidade Materias, definindo as estruturas de dados para criação, atualização e resposta de matérias.
"""

__author__ = ["Gustavo Manganelli", "Erik Santos"]

from typing import Optional
from pydantic import BaseModel


class MateriaBase(BaseModel):
    nome: str
    professor_id: int


class MateriaCreate(MateriaBase):
    pass


class MateriaUpdate(BaseModel):
    nome: Optional[str] = None
    professor_id: Optional[int] = None


class MateriaResponse(MateriaBase):
    id: Optional[int] = None


class MateriaSchema(BaseModel):
    id: int
    nome: str
    professor_id: Optional[int] = None


    class Config:
        from_attributes = True


# backwards compatibility
MateriasSchema = MateriaSchema