from sqlalchemy.orm import Session
from dao.mutante_dao import MutanteDAO
from dao.mutantes_materias_dao import MutantesMateriasDAO
from dao.poder_dao import PoderDAO
from dao.turmas_dao import TurmasDAO
from services.mutante_service import MutanteService
from services.professor_service import ProfessorService
from dao.professor_dao import ProfessorDAO
from dao.materias_dao import MateriasDAO

def verificar_usuario(usuario: str) -> bool:
    return '@' in usuario

def verificar_adm(usuario:str) -> bool:
    return '!' in usuario


def listar_professores(session: Session):
    return ProfessorService(ProfessorDAO(session), MateriasDAO(session)).listar_professores()

def listar_mutantes(session: Session):
    return MutanteService(
        MutanteDAO(session), PoderDAO(session), TurmasDAO(session), MutantesMateriasDAO(session)
    ).listar_mutantes()