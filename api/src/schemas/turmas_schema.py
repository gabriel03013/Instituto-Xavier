from typing import Optional
from pydantic import BaseModel


class TurmaBase(BaseModel):
    serie: int
    turma: str


class TurmaCreate(TurmaBase):
    pass


class TurmaUpdate(BaseModel):
    serie: Optional[int] = None
    turma: Optional[str] = None


class TurmaResponse(TurmaBase):
    id: Optional[int] = None


class TurmaSchema(BaseModel):
    id: int
    serie: int
    turma: str

    class Config:
        from_attributes = True


# compatibility alias
TurmasSchema = TurmaSchema