from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models import Mutante
from typing import List, Optional

class MutanteDAO:
    def __init__(self, session: Session):
        self.session = session


    def criar(self, matricula: str, nome: str, email: str, senha: str, esta_ativo: bool = False, 
              poder_id: Optional[int] = None, turma_id: Optional[int] = None) -> Mutante:
        """Cria um novo mutante."""

        novo_mutante = Mutante(
            matricula=matricula,
            nome=nome,
            email=email,
            senha=senha,
            esta_ativo=esta_ativo,
            poder_id=poder_id,
            turma_id=turma_id
        )
        self.session.add(novo_mutante)
        self.session.commit()
        self.session.refresh(novo_mutante)
        return novo_mutante


    def obter_por_id(self, mutante_id: int) -> Optional[Mutante]:
        """Obtém um mutante pelo ID."""

        return self.session.query(Mutante).filter(Mutante.id == mutante_id).first()


    def obter_por_email(self, email: str) -> Optional[Mutante]:
        """Obtém um mutante pelo email."""

        return self.session.query(Mutante).filter(Mutante.email == email).first()


    def obter_por_matricula(self, matricula: str) -> Optional[Mutante]:
        """Obtém um mutante pela matrícula."""

        return self.session.query(Mutante).filter(Mutante.matricula == matricula).first()


    def obter_matricula_vazia(self, matricula: str) -> Optional[Mutante]:
        """Verifica se a matrícula passada como parâmetro tem o resto de suas credenciais vazias."""

        return self.session.query(Mutante).filter(
            Mutante.matricula == matricula,
            or_(Mutante.nome == None, Mutante.nome == ""),
            or_(Mutante.email == None, Mutante.email == ""),
            or_(Mutante.senha == None, Mutante.senha == ""),
            or_(Mutante.poder_id == None, Mutante.poder_id == 0),
            or_(Mutante.turma_id == None, Mutante.turma_id == 0)
        ).first()


    def listar_todos(self) -> List[Mutante]:
        """Lista todos os mutantes."""

        return self.session.query(Mutante).all()


    def atualizar(self, mutante_id: int, **kwargs) -> Optional[Mutante]:
        """Atualiza um mutante."""

        mutante = self.session.query(Mutante).filter(Mutante.id == mutante_id).first()
        
        if mutante:
            for key, value in kwargs.items():
                if hasattr(mutante, key) and value is not None:
                    setattr(mutante, key, value)

            self.session.commit()
            self.session.refresh(mutante)

        return mutante
    

    def deletar(self, mutante_id: int) -> bool:
        """Deleta um mutante."""

        mutante = self.session.query(Mutante).filter(Mutante.id == mutante_id).first()
        if mutante:
            self.session.delete(mutante)
            self.session.commit()
            return True
        return False