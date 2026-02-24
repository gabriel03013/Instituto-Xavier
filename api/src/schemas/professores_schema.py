from pydantic import BaseModel

class ProfessoresSchemas(BaseModel):
    nome: str
    usuario: str
    senha: str

    class Config:
        from_attributes = True
        