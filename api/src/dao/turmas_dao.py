from sqlalchemy.orm import Session
from models import Turmas
from typing import List, Optional

class TurmasDAO:
    def __init__(self, session: Session):
        self.session = session

    def criar(self, serie: int, turma: str) -> Turmas:
        """Cria uma nova turma."""

        nova_turma = Turmas(serie=serie, turma=turma)
        self.session.add(nova_turma)
        self.session.commit()
        self.session.refresh(nova_turma)
        return nova_turma

    def obter_por_id(self, turma_id: int) -> Optional[Turmas]:
        """Obtém uma turma pelo ID."""

        return self.session.query(Turmas).filter(Turmas.id == turma_id).first()

    def obter_por_serie_e_turma(self, serie: int, turma: str) -> Optional[Turmas]:
        """Obtém uma turma por série e nome."""

        return self.session.query(Turmas).filter(
            (Turmas.serie == serie) & (Turmas.turma == turma)
        ).first()

    def listar_todas(self) -> List[Turmas]:
        """Lista todas as turmas."""

        return self.session.query(Turmas).all()

    def listar_por_serie(self, serie: int) -> List[Turmas]:
        """Lista turmas de uma série."""

        return self.session.query(Turmas).filter(Turmas.serie == serie).all()

    def atualizar(self, turma_id: int, serie: Optional[int] = None, 
                  turma: Optional[str] = None) -> Optional[Turmas]:
        """Atualiza uma turma."""

        turma_obj = self.session.query(Turmas).filter(Turmas.id == turma_id).first()
        if turma_obj:
            if serie is not None:
                turma_obj.serie = serie
            if turma is not None:
                turma_obj.turma = turma
            self.session.commit()
            self.session.refresh(turma_obj)
        return turma_obj

    def deletar(self, turma_id: int) -> bool:
        """Deleta uma turma."""

        turma = self.session.query(Turmas).filter(Turmas.id == turma_id).first()
        if turma:
            self.session.delete(turma)
            self.session.commit()
            return True
        return False