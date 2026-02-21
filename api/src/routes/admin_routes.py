from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from schemas.mutantes_schema import MutanteBase, MutanteCreate
from dependencies import get_session
from database import engine
from dependencies import get_session
from models import Mutante
from db.helpers.security import hash_password 
from dao.mutante_dao import MutanteDAO ########### temporario -> TODO: fazer service 


admin_router = APIRouter(prefix="/admin", tags=["admin"])


@admin_router.get("/health_db")
async def health_db(session: Session = Depends(get_session)):
    """"
    Try connection with database just executing a simple select then returns successful or failure.
    """
    try:
        session.execute(text("SELECT 1"))
        return {"status": "Database connection successful"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )
    

@admin_router.post("/create_registration")
async def create_registration(
    matricula: str,
    session: Session = Depends(get_session)
):
    """
    Admin insere somente a matricula do aluno, que posteriormente vai ser completada na tela de cadastro.
    """
    # TODO -> Criar model, service e schema de admin e arrumar esse codigo
    mutante_dao = MutanteDAO(session=session)

    if mutante_dao.obter_matricula_vazia(matricula):
        raise HTTPException(status_code=400, detail="Matrícula já pertence a alguém.")
    
    mutante_matricula = Mutante()
    mutante_matricula.esta_ativo = False #
    mutante_matricula.matricula = matricula

    session.add(mutante_matricula)
    session.commit()
    session.refresh(mutante_matricula)

    return {"msg": f"Register without credencials created! ID: {mutante_matricula.id}"}
