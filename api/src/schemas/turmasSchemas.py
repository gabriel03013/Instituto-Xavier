from pydantic import BaseModel


class TurmasSchema(BaseModel):
    serie: int
    turma: str

    class Config:
        from_attributes = True