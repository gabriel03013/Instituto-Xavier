from pydantic import BaseModel, EmailStr
from typing import Optional


class MutantCreate(BaseModel):
    nome: str
    matricula: int
    email: EmailStr
    senha: str
    poder_id: int


class MutantUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    poder_id: Optional[int] = None
    turma_id: Optional[int] = None


class MutantSchema(BaseModel):
    id: int
    nome: str
    matricula: int
    email: EmailStr
    senha: str
    poder_id: int

    class Config:
        from_attributes = True