from typing import Optional
from pydantic import BaseModel


class MutantesMateriasBase(BaseModel):
    nota1: float = 0
    nota2: float = 0
    mutante_id: int
    materia_id: int


class MutantesMateriasCreate(MutantesMateriasBase):
    pass


class MutantesMateriasUpdate(BaseModel):
    nota1: Optional[float] = None
    nota2: Optional[float] = None
    mutante_id: Optional[int] = None
    materia_id: Optional[int] = None


class MutantesMateriasResponse(MutantesMateriasBase):
    id: Optional[int] = None


class MutantesMateriasSchema(BaseModel):
    id: int
    nota1: float
    nota2: float
    mutante_id: int
    materia_id: int

    class Config:
        from_attributes = True


class MutanteGradeSchema(BaseModel):
    id: int
    nome: str
    matricula: str
    nota1: float
    nota2: float
    media: float

    class Config:
        from_attributes = True


# old name alias
MutantesMateriasSchemas = MutantesMateriasSchema