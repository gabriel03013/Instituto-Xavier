from pydantic import BaseModel


class PoderSchema(BaseModel):
    nome: str

    class Config:
        from_attributes = True