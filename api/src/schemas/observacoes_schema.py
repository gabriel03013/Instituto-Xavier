from pydantic import BaseModel
from sqlalchemy import Date


class ObservacoesSchemas(BaseModel):
    observacao: str
    data: Date
    mutantesmaterias_id: int

    class Config:
        from_attributes = True