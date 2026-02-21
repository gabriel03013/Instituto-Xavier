from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy import Boolean


class MutanteBase(BaseModel):
    id: Optional[int]
    nome: Optional[str] = None
    matricula: str
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    # esta_ativo: Optional[Boolean] = False
    poder_id: Optional[int]
    turma_id: Optional[int]

    class Config:
        from_attributes = True


class MutanteCreate(BaseModel):
    nome: str
    matricula: str
    email: EmailStr
    senha: str

    class Config:
        from_attributes = True


class MutanteUpdate(BaseModel):
    nome: Optional[str] = None
    matricula: str
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    esta_ativo: Optional[bool] = False
    poder_id: Optional[int]
    turma_id: Optional[int]


class MutanteResponse(MutanteBase):
    id: Optional[int]

    class Config:
        from_attributes = True