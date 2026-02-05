from pydantic import BaseModel, EmailStr

class MutantSchema(BaseModel):
    nome: str
    matricula: int
    email: EmailStr
    senha: str

    class config:
        from_attributes = True