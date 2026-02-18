from pydantic import BaseModel

class MateriasCreate(BaseModel):
    nome: str
    professor_id: int


class MateriasRead(BaseModel):
    id: int
    nome: str
    professor_id: int

    class config:
        from_attributes = True