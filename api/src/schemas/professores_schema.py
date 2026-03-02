from typing import Optional, List
from pydantic import BaseModel
from schemas.materias_schema import MateriaSchema


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
    materias: List[MateriaSchema] = []

    class Config:
        from_attributes = True


# maintain old name for backwards compatibility
ProfessoresSchemas = ProfessorSchema
        