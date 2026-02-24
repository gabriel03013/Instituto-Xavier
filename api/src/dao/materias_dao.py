from sqlalchemy.orm import Session
from models import Materias
from typing import List, Optional

class MateriasDAO:
    def __init__(self, session: Session):
        self.session = session

    def criar(self, nome: str, professor_id: int) -> Materias:
        """Cria uma nova matéria."""

        nova_materia = Materias(nome=nome, professor_id=professor_id)
        self.session.add(nova_materia)
        self.session.commit()
        self.session.refresh(nova_materia)
        return nova_materia

    def obter_por_id(self, materia_id: int) -> Optional[Materias]:
        """Obtém uma matéria pelo ID."""

        return self.session.query(Materias).filter(Materias.id == materia_id).first()

    def obter_por_nome(self, nome: str) -> Optional[Materias]:
        """Obtém uma matéria pelo nome."""

        return self.session.query(Materias).filter(Materias.nome == nome).first()

    def listar_todas(self) -> List[Materias]:
        """Lista todas as matérias."""

        return self.session.query(Materias).all()

    def listar_por_professor(self, professor_id: int) -> List[Materias]:
        """Lista matérias de um professor."""

        return self.session.query(Materias).filter(Materias.professor_id == professor_id).all()

    def atualizar(self, materia_id: int, **kwargs) -> Optional[Materias]:
        """Atualiza uma matéria existente."""

        materia = self.session.query(Materias).filter(Materias.id == materia_id).first()
        if materia:
            for key, value in kwargs.items():
                if hasattr(materia, key) and value is not None:
                    setattr(materia, key, value)
            self.session.commit()
            self.session.refresh(materia)
        return materia

    def deletar(self, materia_id: int) -> bool:
        """Deleta uma matéria."""

        materia = self.session.query(Materias).filter(Materias.id == materia_id).first()
        if materia:
            self.session.delete(materia)
            self.session.commit()
            return True
        return False