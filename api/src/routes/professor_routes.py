"""
Classe de rotas para o recurso de professor, responsável por definir os endpoints relacionados aos professores, como listar, 
criar, obter detalhes, atualizar e deletar professores. Além disso, inclui um endpoint para obter o dashboard do professor,
que apresenta informações relevantes sobre os alunos e suas notas.
"""

__author__ = ["Gabriel Mendes", "Erik Santos", "Davi Franco"]

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_session
from dao.professor_dao import ProfessorDAO
from dao.materias_dao import MateriasDAO
from api.src.dao.dashboards_dao import DashboardsDAO
from services.professor_service import ProfessorService
from schemas.professores_schema import ProfessorCreate, ProfessorUpdate, ProfessorSchema


professor_router = APIRouter(prefix="/professor", tags=["professor"])


def get_professor_service(session: Session = Depends(get_session)) -> ProfessorService:
    """
    Retorna uma instância do ProfessorService, que é responsável por lidar com a lógica de negócios relacionada aos professores.

    Args:
        session (Session, optional): Sessão do banco de dados. Defaults to Depends(get_session).

    Returns:
        ProfessorService: service com as dependências necessárias para as operações relacionadas ao professor
    """
    professor_dao = ProfessorDAO(session)
    materias_dao = MateriasDAO(session)
    return ProfessorService(professor_dao, materias_dao)

@professor_router.get("/", response_model=List[ProfessorSchema])
async def listar_professores(service: ProfessorService = Depends(get_professor_service)) -> List[ProfessorSchema]:
    """
    Lista todos os professores cadastrados no sistema.

    Args:
        service (ProfessorService, optional): Sessão do serviço de professor. Defaults to Depends(get_professor_service).

    Returns:
        List[ProfessorSchema]: Lista de professores cadastrados no sistema
    """
    
    return service.listar_professores()


@professor_router.post("/", response_model=ProfessorSchema, status_code=status.HTTP_201_CREATED)
async def criar_professor(dados: ProfessorCreate, service: ProfessorService = Depends(get_professor_service)) -> ProfessorSchema:
    """
    Cria um novo professor no sistema.

    Args:
        dados (ProfessorCreate): Dados do professor a ser criado
        service (ProfessorService, optional): Sessão do serviço de professor. Defaults to Depends(get_professor_service).

    Returns:
        ProfessorSchema: Professor criado no sistema
    """
    
    try:
        return service.criar_novo_professor(dados)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@professor_router.get("/dashboard")
async def get_dashboard(
    id_professor: int,
    session: Session = Depends(get_session)
) -> dict:
    """
    Dashboard para visualização de Total de alunos, Média de notas e Total de observações.
    
    Args:
        id_professor (int): ID do professor para filtrar os dados do dashboard
    
    Returns:
        dict: Dicionário contendo os dados do dashboard, incluindo total de alunos, média de notas e total de observações
    """
    dashboard_dao = DashboardsDAO(session=session)
    dash = dashboard_dao.obter_kpis_professor(id_professor=int(id_professor))
    nota_turma_materia = dashboard_dao.obter_notas_por_turma_materia(id_professor=int(id_professor))
    situacao_alunos = dashboard_dao.obter_situacao_alunos(id_professor=int(id_professor))
    return {
        "dashboard": dash,
        "notas_turma_materia": nota_turma_materia,
        "situacao_alunos": situacao_alunos
    }


@professor_router.get("/{professor_id}", response_model=ProfessorSchema)
async def obter_professor(professor_id: int, service: ProfessorService = Depends(get_professor_service)) -> ProfessorSchema:
    """
    Rota para obter os detalhes de um professor específico com base no ID fornecido. Se o professor não for encontrado, 
    uma exceção HTTP 404 será lançada.

    Args:
        professor_id (int): ID do professor
        service (ProfessorService, optional): Service do professor. Defaults to Depends(get_professor_service).

    Raises:
        HTTPException: exceção lançada quando o professor não é encontrado, com status code 404 e mensagem de erro detalhada

    Returns:
        ProfessorSchema: Professor encontrado, retornado como um objeto ProfessorSchema
    """
    
    try:
        return service.obter_professor_por_id(professor_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@professor_router.patch("/{professor_id}", response_model=ProfessorSchema)
async def atualizar_professor(professor_id: int, dados: ProfessorUpdate, service: ProfessorService = Depends(get_professor_service)) -> ProfessorSchema:
    """
    Rota para atualizar os dados de um professor específico com base no ID fornecido.

    Args:
        professor_id (int): ID do professor a ser atualizado
        dados (ProfessorUpdate): Dados atualizados do professor
        service (ProfessorService, optional): Service do professor. Defaults to Depends(get_professor_service).

    Returns:
        ProfessorSchema: Professor atualizado, retornado como um objeto ProfessorSchema
    """

    try:
        return service.atualizar_professor(professor_id, dados)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@professor_router.delete("/{professor_id}")
async def deletar_professor(professor_id: int, service: ProfessorService = Depends(get_professor_service)) -> dict:
    """
    Rota para deletar um professor específico com base no ID fornecido. Se o professor não for encontrado, 
    uma exceção HTTP 404 será lançada.

    Args:
        professor_id (int): ID do professor a ser deletado
        service (ProfessorService, optional): Service do professor. Defaults to Depends(get_professor_service).

    Raises:
        HTTPException: exceção lançada quando o professor não é encontrado, com status code 404 e mensagem de erro detalhada

    Returns:
        dict: Dicionário contendo uma mensagem de sucesso ou erro
    """
    
    try:
        return service.deletar_professor(professor_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))