"""
Classe DAO para a entidade Turmas, responsável por realizar as operações de CRUD (Create, Read, Update, Delete)
"""

__author__ = "Davi Franco"

from sqlalchemy.orm import Session
from models import Turmas, Mutante
from typing import List, Optional

class TurmasDAO:
    def __init__(self, session: Session):
        self.session = session

    def criar(self, serie: int, turma: str) -> Turmas:
        """
        Cria uma nova turma.
        
        Args:
            serie (int): Serie de turmas
            turma (str): Nome da turma
            
        Returns:
            Turmas: A turma criada no sistema.
        """

        nova_turma = Turmas(serie=serie, turma=turma)
        self.session.add(nova_turma)
        self.session.commit()
        self.session.refresh(nova_turma)
        return nova_turma

    def obter_por_id(self, turma_id: int) -> Optional[Turmas]:
        """
        Obtém uma turma pelo ID com carregamento otimizado de alunos e suas notas.
        
        Args:
            turma_id (int): ID da turma a ser obtida.
            
        Returns:
            Optional[Turmas]: Turma encontrada ou None se não encontrada.
        """
        from sqlalchemy.orm import joinedload
        return self.session.query(Turmas)\
            .options(joinedload(Turmas.mutantes).joinedload(Mutante.mutantesmaterias))\
            .filter(Turmas.id == turma_id).first()

    def obter_por_serie_e_turma(self, serie: int, turma: str) -> Optional[Turmas]:
        """
        Obtém uma turma por série e nome.
        
        Args:
            serie (int): Série da turma.
            turma (str): Nome da turma.
            
        Returns:
            Optional[Turmas]: Turma encontrada ou None se não encontrada.
        """

        return self.session.query(Turmas).filter(
            (Turmas.serie == serie) & (Turmas.turma == turma)
        ).first()

    def listar_todas(self) -> List[Turmas]:
        """
        Lista todas as turmas.
        
        Returns:
            List[Turmas]: Lista de todas as turmas cadastradas no sistema.            
        """

        from sqlalchemy.orm import joinedload
        return self.session.query(Turmas)\
            .options(joinedload(Turmas.mutantes).joinedload(Mutante.mutantesmaterias))\
            .all()

    def listar_por_serie(self, serie: int) -> List[Turmas]:
        """
        Lista turmas de uma série.
        
        Args:
            serie (int): Série das turmas a serem listadas.
            
        Returns:
            List[Turmas]: Lista de turmas da série especificada.
        """

        from sqlalchemy.orm import joinedload
        return self.session.query(Turmas)\
            .options(joinedload(Turmas.mutantes).joinedload(Mutante.mutantesmaterias))\
            .filter(Turmas.serie == serie)\
            .all()

    def atualizar(self, turma_id: int, serie: Optional[int] = None, 
                  turma: Optional[str] = None) -> Optional[Turmas]:
        """
        Atualiza uma turma.
        
        Args:
            turma_id (int): ID da turma a ser atualizada.
            serie (Optional[int]): Nova série da turma (opcional).
            turma (Optional[str]): Novo nome da turma (opcional).
        
        Returns:
            Optional[Turmas]: Turma atualizada ou None se a turma não for encontrada.
        """

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
        """
        Deleta uma turma baseado no ID recebido.
        
        Args:
            turma_id (int): ID da turma a ser deletada.
        
        Returns:
            bool: True se a turma foi deletada, False se a turma não foi encontrada.
        """

        turma = self.session.query(Turmas).filter(Turmas.id == turma_id).first()
        if turma:
            self.session.delete(turma)
            self.session.commit()
            return True
        return False