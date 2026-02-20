from pydantic import BaseModel, EmailStr


class MutanteSchema(BaseModel):
    nome: str
    matricula: int
    email: EmailStr
    senha: str
    poder_id: int
    turma_id: int

    class Config:
        from_attributes = True