from pydantic import BaseModel


class MateriasSchema(BaseModel):
    nome: str
    professor_id: int

    class Config:
        from_attributes = True