from pydantic import BaseModel, EmailStr
from typing import Optional


class MutanteSchema(BaseModel):
    nome: str
    matricula: int
    email: EmailStr
    senha: str
    poder_id: int
    turma_id: int

<<<<<<< HEAD

class MutantUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    poder_id: Optional[int] = None
    turma_id: Optional[int] = None


class MutantSchema(BaseModel):
    id: int
    nome: str
    matricula: int
    email: EmailStr
    senha: str
    poder_id: int

=======
>>>>>>> 6f24b8e149ddeddadd591e7df4bd65379b291eaf
    class Config:
        from_attributes = True