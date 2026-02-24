from sqlalchemy.orm import Session
from models import Poder
from typing import List, Optional

class PoderDAO:
    def __init__(self, session: Session):
        self.session = session

    def criar(self, nome: str) -> Poder:
        """Cria um novo poder."""

        novo_poder = Poder(nome=nome)
        self.session.add(novo_poder)
        self.session.commit()
        self.session.refresh(novo_poder)
        return novo_poder

    def obter_por_id(self, poder_id: int) -> Optional[Poder]:
        """Obtém um poder pelo ID."""

        return self.session.query(Poder).filter(Poder.id == poder_id).first()

    def obter_por_nome(self, nome: str) -> Optional[Poder]:
        """Obtém um poder pelo nome."""

        return self.session.query(Poder).filter(Poder.nome == nome).first()

    def listar_todos(self) -> List[Poder]:
        """Lista todos os poderes."""

        return self.session.query(Poder).all()

    def atualizar(self, poder_id: int, nome: str) -> Optional[Poder]:
        """Atualiza um poder."""

        poder = self.session.query(Poder).filter(Poder.id == poder_id).first()
        if poder:
            poder.nome = nome
            self.session.commit()
            self.session.refresh(poder)
        return poder

    def deletar(self, poder_id: int) -> bool:
        """Deleta um poder."""

        poder = self.session.query(Poder).filter(Poder.id == poder_id).first()
        if poder:
            self.session.delete(poder)
            self.session.commit()
            return True
        return False