from pydantic import BaseModel


class PoderCreate(BaseModel):
    id: int
    nome: str

class PoderRead(BaseModel):
    nome: str

    class config:
        from_attributes = True