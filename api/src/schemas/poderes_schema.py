"""
Schemas Pydantic para a entidade Materias, definindo as estruturas de dados para criação, atualização e resposta de matérias.
"""

__author__ = ["Gustavo Manganelli", "Erik Santos"]

from typing import Optional
from pydantic import BaseModel


class PoderBase(BaseModel):
    nome: str


class PoderCreate(PoderBase):
    pass


class PoderUpdate(BaseModel):
    nome: Optional[str] = None


class PoderResponse(PoderBase):
    id: Optional[int] = None


class PoderSchema(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True


# old class alias
PoderesSchema = PoderSchema