from pydantic import BaseModel, EmailStr


class MutanteSchema(BaseModel):
    nome: str
    matricula: str
    email: EmailStr
    senha: str


class MutanteUpdate(BaseModel):
    nome: Optional[str] = None
    matricula: str
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    esta_ativo: Optional[bool] = False
    poder_id: Optional[int]
    turma_id: Optional[int]


class MutanteResponse(MutanteBase):
    id: Optional[int]

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