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


class MutanteInfoSchema(BaseModel):
    id: int
    nome: str
    turma: str

    class Config:
        from_attributes = True


class MutanteMateriaInfoSchema(BaseModel):
    materia_id: int
    materia: str
    professor: str

    class Config:
        from_attributes = True


class MutanteBase(BaseModel):
    nome: str
    matricula: str
    email: str
    senha: str
    turma_id: Optional[int] = None



class MutanteCreate(MutanteBase):
    pass


class MutanteUpdate(BaseModel):
    nome: Optional[str] = None
    matricula: str
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    esta_ativo: Optional[bool] = False
    turma_id: Optional[int] = None


class MutanteResponse(MutanteBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True


class MutanteSchema(BaseModel):
    id: int
    nome: str
    matricula: str
    email: str
    senha: str
    turma_id: Optional[int] = None


    class Config:
        from_attributes = True


class ResetPasswordSchema(BaseModel):
    chave_seguranca: str
    nova_senha: str