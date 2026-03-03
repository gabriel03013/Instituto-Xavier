from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_session
from dao.professor_dao import ProfessorDAO
from dao.materias_dao import MateriasDAO
from dao.dashboards import DashboardsDAO
from services.professor_service import ProfessorService
from schemas.professores_schema import ProfessorCreate, ProfessorUpdate, ProfessorSchema


professor_router = APIRouter(prefix="/professor", tags=["professor"])


def get_professor_service(
    session: Session = Depends(get_session)
) -> ProfessorService:
    professor_dao = ProfessorDAO(session)
    materias_dao = MateriasDAO(session)
    return ProfessorService(professor_dao, materias_dao)

@professor_router.get("/", response_model=List[ProfessorSchema])
async def listar_professores(
    service: ProfessorService = Depends(get_professor_service)
):
    return service.listar_professores()


@professor_router.post("/", response_model=ProfessorSchema, status_code=status.HTTP_201_CREATED)
async def criar_professor(
    dados: ProfessorCreate, 
    service: ProfessorService = Depends(get_professor_service)
):
    try:
        return service.criar_novo_professor(dados)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@professor_router.get("/dashboard")
async def get_dashboard(
    id_professor: int,
    session: Session = Depends(get_session)
):
    """
    Dashboard para visualização de Total de alunos, Média de notas e Total de observações.
    """
    dashboard_dao = DashboardsDAO(session=session)
    dash = dashboard_dao.obter_dashboard_professor(id_professor=int(id_professor))
    return dash


@professor_router.get("/{professor_id}", response_model=ProfessorSchema)
async def obter_professor(
    professor_id: int, 
    service: ProfessorService = Depends(get_professor_service)
):
    try:
        return service.obter_professor_por_id(professor_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@professor_router.patch("/{professor_id}", response_model=ProfessorSchema)
async def atualizar_professor(
    professor_id: int, dados: ProfessorUpdate, 
    service: ProfessorService = Depends(get_professor_service)
):
    try:
        return service.atualizar_professor(professor_id, dados)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@professor_router.delete("/{professor_id}")
async def deletar_professor(
    professor_id: int, 
    service: ProfessorService = Depends(get_professor_service)
):
    try:
        return service.deletar_professor(professor_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))