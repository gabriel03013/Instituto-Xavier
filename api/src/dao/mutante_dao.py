from sqlalchemy.orm import Session
from models import Mutant
from typing import List, Optional

class MutanteDAO:
    def __init__(self, session: Session):
        self.session = session

    def criar(self, matricula: str, nome: str, email: str, senha: str, 
              poder_id: Optional[int] = None, turma_id: Optional[int] = None) -> Mutant:
        """Cria um novo mutante."""

        novo_mutante = Mutant(
            matricula=matricula,
            nome=nome,
            email=email,
            senha=senha,
            poder_id=poder_id,
            turma_id=turma_id
        )
        self.session.add(novo_mutante)
        self.session.commit()
        self.session.refresh(novo_mutante)
        return novo_mutante

    def obter_por_id(self, mutante_id: int) -> Optional[Mutant]:
        """Obtém um mutante pelo ID."""

        return self.session.query(Mutant).filter(Mutant.id == mutante_id).first()

    def obter_por_email(self, email: str) -> Optional[Mutant]:
        """Obtém um mutante pelo email."""

        return self.session.query(Mutant).filter(Mutant.email == email).first()

    def obter_por_matricula(self, matricula: str) -> Optional[Mutant]:
        """Obtém um mutante pela matrícula."""

        return self.session.query(Mutant).filter(Mutant.matricula == matricula).first()

    def listar_todos(self) -> List[Mutant]:
        """Lista todos os mutantes."""

        return self.session.query(Mutant).all()

    def atualizar(self, mutante_id: int, **kwargs) -> Optional[Mutant]:
        """Atualiza um mutante."""

        mutante = self.session.query(Mutant).filter(Mutant.id == mutante_id).first()
        if mutante:
            for key, value in kwargs.items():
                if hasattr(mutante, key) and value is not None:
                    setattr(mutante, key, value)
            self.session.commit()
            self.session.refresh(mutante)
        return mutante

    def deletar(self, mutante_id: int) -> bool:
        """Deleta um mutante."""

        mutante = self.session.query(Mutant).filter(Mutant.id == mutante_id).first()
        if mutante:
            self.session.delete(mutante)
            self.session.commit()
            return True
        return False