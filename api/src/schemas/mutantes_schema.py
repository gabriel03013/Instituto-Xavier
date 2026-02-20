from pydantic import BaseModel, EmailStr


class MutantesSchema(BaseModel):
    nome: str
    matricula: str
    email: EmailStr
    senha: str
    poder_id: int
    turma_id: int

    class Config:
        from_attributes = True


class MutantesCreate(BaseModel):
    nome: str
    matricula: str
    email: EmailStr
    senha: str

    class Config:
        from_attributes = True