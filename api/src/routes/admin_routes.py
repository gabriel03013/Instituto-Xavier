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
from dao.dashboards_dao import DashboardsDAO


admin_router = APIRouter(prefix="/admin", tags=["admin"])


@admin_router.get("/health_db")
async def health_db(session: Session = Depends(get_session)):
    """"
    Verifica a saúde da conexão com o banco de dados executando
    uma consulta simples.

    Args:
        session (Session): Dependência da sessão do banco de dados.

    Returns:
        dict: Dicionário indicando sucesso da conexão com o banco.
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
    turma_id: int = None,
    session: Session = Depends(get_session)
):
    """
    Cria um registro inicial de matrícula para um aluno.
    O administrador insere apenas a matrícula do aluno, permitindo
    que o restante das informações seja preenchido posteriormente
    pelo próprio usuário durante o cadastro.
    
    Args:
        matricula (str): Matrícula do aluno a ser criada.
        turma_id (int, optional): ID da turma a ser associada ao aluno.
        session (Session): Database session dependency.
        
    Returns:
        dict: Mensagem de sucesso com o ID do registro criado.
    """
    mutante_dao = MutanteDAO(session=session)

    if mutante_dao.obter_por_matricula(matricula):
        raise HTTPException(status_code=400, detail="Matrícula já existe ou pertence a alguém.")
    
    mutante_matricula = Mutante()
    mutante_matricula.nome = ""
    mutante_matricula.email = f"pending_{matricula}@placeholder"
    mutante_matricula.senha = ""
    mutante_matricula.esta_ativo = False
    mutante_matricula.chave_seguranca = ""
    mutante_matricula.matricula = matricula
    if turma_id:
        mutante_matricula.turma_id = turma_id

    session.add(mutante_matricula)
    session.commit()
    session.refresh(mutante_matricula)

    return {"msg": f"Register without credencials created! ID: {mutante_matricula.id}"}


@admin_router.get("/kpis")
async def get_kpis(
    session: Session = Depends(get_session)
):
    """
    Retorna os principais indicadores (KPIs) para o dashboard administrativo.
    Os dados incluem o total de alunos, professores e turmas
    cadastrados no sistema.

    Args:
        session (Session): Dependência da sessão do banco de dados.

    Returns:
        dict: Dicionário contendo:
            - total_alunos (int): Quantidade total de alunos cadastrados.
            - total_professores (int): Quantidade total de professores cadastrados.
            - total_turmas (int): Quantidade total de turmas cadastradas.
    """
    dashboards_dao = DashboardsDAO(session=session)

    return dashboards_dao.obter_kpis_admin()


@admin_router.get('/visao-geral')
async def get_statistics(
    session: Session = Depends(get_session)
):
    """
    Retorna a média de notas agrupada por turma e matéria para visualização
    em gráficos administrativos.
    Os dados são utilizados para compor gráficos (ex: barras) que mostram
    o desempenho médio das turmas em cada matéria.

    Args:
        session (Session): Dependência da sessão do banco de dados.

    Returns:
        list[dict]: Lista de objetos contendo:
            - turma (str): Nome da turma no formato "Xº Ano Y".
            - materia (str): Nome da matéria.
            - media (float): Média das notas dos alunos naquela turma e matéria.
    """
    dashboards_dao = DashboardsDAO(session=session)

    nota_turma_materia = dashboards_dao.obter_grafico_admin()

    return [
        {"turma": result["turma"], "materia": result["materia"], "media": float(result["media"])}
        for result in nota_turma_materia
    ]