from pydantic import BaseModel

class ProfessorCreate(BaseModel):
    nome: str
    usuario: str
    senha: str

class ProfessorRead(BaseModel):
    id: int
    nome: str
    usuario: str
    senha: str

    class config:
        from_attributes = True
        