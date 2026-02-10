from pydantic import BaseModel, EmailStr

class MutesntesMateriasCreate(BaseModel):
    mutante_id: int
    materia_id: int
    nota_1: float
    nota_2: float
    observacao: str
    

class MutesntesMateriasRead(BaseModel):
    mutante_id: int
    materia_id: int
    nota_1: float
    nota_2: float
    observacao: str
    
    class config:
        from_attributes = True    