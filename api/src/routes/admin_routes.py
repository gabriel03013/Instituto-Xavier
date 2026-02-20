from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from schemas.mutantes_schema import MutantesSchema, MutantesCreate
from dependencies import get_session
from database import engine
from dependencies import get_session
from models import Mutantes
from db.helpers.security import hash_password 


admin_router = APIRouter(prefix="/admin", tags=["admin"])


@admin_router.post("/inserir_matricula")
async def inserir_matricula(
    matricula: str,
    session: Session = Depends(get_session)
):
    """
    Admin insere somente a matricula do aluno, que posteriormente vai completar o cadastro.
    """
    mutante_matricula = Mutantes()
    mutante_matricula.matricula = matricula

    session.add(mutante_matricula)