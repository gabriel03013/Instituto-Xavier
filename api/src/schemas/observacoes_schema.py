from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Date


class ObservacaoBase(BaseModel):
    observacao: str
    data: Date
    mutantesmaterias_id: int


class ObservacaoCreate(ObservacaoBase):
    pass


class ObservacaoUpdate(BaseModel):
    observacao: Optional[str] = None
    data: Optional[Date] = None
    mutantesmaterias_id: Optional[int] = None


class ObservacaoResponse(ObservacaoBase):
    id: Optional[int] = None


class ObservacaoSchema(BaseModel):
    id: int
    observacao: str
    data: Date
    mutantesmaterias_id: int

    class Config:
        from_attributes = True


# alias for compatibility
ObservacoesSchemas = ObservacaoSchema