from typing import Annotated, Optional, Literal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth_utils import listar_mutantes, listar_professores

from dependencies import get_session

from dao.mutante_dao import MutanteDAO
from dao.mutantes_materias_dao import MutantesMateriasDAO
from dao.poder_dao import PoderDAO
from dao.turmas_dao import TurmasDAO
from services.mutante_service import MutanteService

from services.professor_service import ProfessorService
from dao.professor_dao import ProfessorDAO
from dao.materias_dao import MateriasDAO

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    id: int
    nome: str
    identificador: str  # mutante: email | professor: usuario
    tipo: Literal["mutante", "professor"]


def decode_token(token: str, session: Session) -> Optional[User]:
    
    for m in listar_mutantes(session): # Carregando todos os mutantes do banco
        if getattr(m, "email", None) == token:
            return User(id=m.id, nome=m.nome, identificador=m.email, tipo="mutante")

    for p in listar_professores(session): # Carregando todos os professores do banco
        if getattr(p, "usuario", None) == token:
            return User(id=p.id, nome=p.nome, identificador=p.usuario, tipo="professor")

    return None

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],session: Session = Depends(get_session)) -> User:
    user = decode_token(token, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user