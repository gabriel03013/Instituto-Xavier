"""
Rotas administrativas para o sistema, destinadas ao uso por administradores.
Oferece endpoints para verificar a saúde da conexão com o banco de dados e
criar registros de matrícula vazios que serão completados posteriormente.

Algumas funcionalidades são temporárias e possuem TODOs de refatoração.
"""

__author__ = "Erik Santos"

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from dependencies import get_session
from database import engine
from models import Mutante
from db.helpers.security import hash_password 
from dao.mutante_dao import MutanteDAO 
from api.src.dao.dashboards_dao import DashboardsDAO


admin_router = APIRouter(prefix="/admin", tags=["admin"])


@admin_router.get("/health_db")
async def health_db(session: Session = Depends(get_session)):
    """"
    Try connection with database just executing a simple select then returns successful or failure.
    
    Args:
        session (Session): Database session dependency.
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
    
    Args:
        matricula (str): Matrícula do aluno a ser criada.
        session (Session): Database session dependency.
        
    Returns:
        dict: Mensagem de sucesso com o ID do registro criado.
    """
    # TODO -> Criar model, service e schema de admin e arrumar esse codigo
    mutante_dao = MutanteDAO(session=session)

    if mutante_dao.obter_matricula_vazia(matricula):
        raise HTTPException(status_code=400, detail="Matrícula já existe ou pertence a alguém.")
    
    mutante_matricula = Mutante()
    mutante_matricula.esta_ativo = False #
    mutante_matricula.matricula = matricula

    session.add(mutante_matricula)
    session.commit()
    session.refresh(mutante_matricula)

    return {"msg": f"Register without credencials created! ID: {mutante_matricula.id}"}


@admin_router.get("/kpis")
async def get_kpis(
    session: Session = Depends(get_session)
):
    """
    KPIs que contém o total de Alunos, total de Professores e total de Turmas para visualização do Admin
    """
    dashboards_dao = DashboardsDAO(session=session)

    return dashboards_dao.obter_kpis_admin()