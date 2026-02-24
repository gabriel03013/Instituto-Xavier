from typing import Optional
from pydantic import BaseModel


class MutantesMateriasBase(BaseModel):
    nota_1: float
    nota_2: float
    mutante_id: int
    materia_id: int


class MutantesMateriasCreate(MutantesMateriasBase):
    pass


class MutantesMateriasUpdate(BaseModel):
    nota_1: Optional[float] = None
    nota_2: Optional[float] = None
    mutante_id: Optional[int] = None
    materia_id: Optional[int] = None


class MutantesMateriasResponse(MutantesMateriasBase):
    id: Optional[int] = None


class MutantesMateriasSchema(BaseModel):
    id: int
    nota_1: float
    nota_2: float
    mutante_id: int
    materia_id: int

    class Config:
        from_attributes = True


# old name alias
MutantesMateriasSchemas = MutantesMateriasSchema