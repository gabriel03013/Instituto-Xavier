from pydantic import BaseModel, EmailStr


class MutantCreate(BaseModel):
    nome: str
    matricula: int
    email: EmailStr
    senha: str
    poder_id: int

class MutantRead(BaseModel):
    id: int
    nome: str
    matricula: int
    email: EmailStr
    senha: str
    poder_id: int

    class config:
        from_attributes = True
        