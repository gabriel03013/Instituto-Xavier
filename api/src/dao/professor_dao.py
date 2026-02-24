from sqlalchemy.orm import Session
from models import Professor
from typing import List, Optional

class ProfessorDAO:
    def __init__(self, session: Session):
        self.session = session

    def criar(self, nome: str, usuario: str, senha: str) -> Professor:
        """Cria um novo professor."""

        novo_professor = Professor(nome=nome, usuario=usuario, senha=senha)
        self.session.add(novo_professor)
        self.session.commit()
        self.session.refresh(novo_professor)
        return novo_professor

    def obter_por_id(self, professor_id: int) -> Optional[Professor]:
        """Obtém um professor pelo ID."""

        return self.session.query(Professor).filter(Professor.id == professor_id).first()

    def obter_por_usuario(self, usuario: str) -> Optional[Professor]:
        """Obtém um professor pelo usuário."""

        return self.session.query(Professor).filter(Professor.usuario == usuario).first()

    def listar_todos(self) -> List[Professor]:
        """Lista todos os professores."""

        return self.session.query(Professor).all()

    def atualizar(self, professor_id: int, **kwargs) -> Optional[Professor]:
        """Atualiza um professor."""

        professor = self.session.query(Professor).filter(Professor.id == professor_id).first()
        if professor:
            for key, value in kwargs.items():
                if hasattr(professor, key) and value is not None:
                    setattr(professor, key, value)
            self.session.commit()
            self.session.refresh(professor)
        return professor

    def deletar(self, professor_id: int) -> bool:
        """Deleta um professor."""

        professor = self.session.query(Professor).filter(Professor.id == professor_id).first()
        if professor:
            self.session.delete(professor)
            self.session.commit()
            return True
        return False