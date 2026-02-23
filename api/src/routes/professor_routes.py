from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session
from dao.dashboard_professor import DashboardProfessorDAO


professor_router = APIRouter(prefix="/professor", tags=["professor"])


@professor_router.get("/")
async def home():
    return {"msg": "Welcome, professor"}


@professor_router.get("/dashboard")
async def get_dashboard(
    id_professor: int,
    session: Session = Depends(get_session)
):
    """
    Dashboard para visualização de Total de alunos, Média de notas e Total de observações.
    """
    dashboard_dao = DashboardProfessorDAO(session=session)

    dash = dashboard_dao.obter_dashboard(id_professor=id_professor)

    return dash