from pydantic import BaseModel, EmailStr
from typing import Optional


class MutantesMateriasSchemas(BaseModel):
    nota_1: float
    nota_2: float
    mutante_id: int
    materia_id: int

    class Config:
        from_attributes = True