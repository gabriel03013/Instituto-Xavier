"""
Schemas Pydantic para a entidade Materias, definindo as estruturas de dados para criação, atualização e resposta de matérias.
"""

__author__ = ["Gustavo Manganelli", "Erik Santos"]

from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date


class MutanteSimpleSchema(BaseModel):
    id: int
    nome: str
    matricula: str

    class Config:
        from_attributes = True


class MutanteBase(BaseModel):
    nome: str
    matricula: str
    email: EmailStr
    senha: str


class MutanteCreate(MutanteBase):
    pass


class MutanteUpdate(BaseModel):
    nome: Optional[str] = None
    matricula: str
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    esta_ativo: Optional[bool] = False
    poder_id: Optional[int] = None
    turma_id: Optional[int] = None


class MutanteResponse(MutanteBase):
    id: Optional[int] = None


class MutanteSchema(BaseModel):
    id: int
    nome: str
    matricula: str
    email: EmailStr
    senha: str
    poder_id: int

    class Config:
        from_attributes = True