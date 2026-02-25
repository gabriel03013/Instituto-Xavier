from typing import Optional
from pydantic import BaseModel


class ProfessorBase(BaseModel):
    nome: str
    usuario: str
    senha: str


class ProfessorCreate(ProfessorBase):
    """Schema used when creating a new professor."""
    pass


class ProfessorUpdate(BaseModel):
    nome: Optional[str] = None
    usuario: Optional[str] = None
    senha: Optional[str] = None


class ProfessorResponse(ProfessorBase):
    id: Optional[int] = None


class ProfessorSchema(BaseModel):
    id: int
    nome: str
    usuario: str
    senha: str

    class Config:
        from_attributes = True


# maintain old name for backwards compatibility
ProfessoresSchemas = ProfessorSchema
        