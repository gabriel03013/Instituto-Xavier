"""
Classe DAO para a entidade Materias, responsável por realizar as operações de CRUD (Create, Read, Update, Delete) 
relacionadas às matérias. Esta classe fornece métodos para criar novas matérias, obter matérias por ID ou nome, listar todas 
as matérias ou as matérias de um professor específico, atualizar os detalhes de uma matéria existente e deletar uma matéria 
do sistema.
"""

__author__ = "Davi Franco"

from sqlalchemy.orm import Session
from models import Materias
from typing import List, Optional

class MateriasDAO:
    def __init__(self, session: Session):
        self.session = session
    

    
    def criar(self, nome: str, professor_id: int) -> Materias:
        """
        Cria uma nova matéria.
        
        Args:
            nome (str): Nome da matéria.
            professor_id (int): ID do professor responsável pela matéria.

        Returns:
            Materias: Nova matéria criada.
        """

        nova_materia = Materias(nome=nome, professor_id=professor_id)
        self.session.add(nova_materia)
        self.session.commit()
        self.session.refresh(nova_materia)
        return nova_materia

    def obter_por_id(self, materia_id: int) -> Optional[Materias]:
        """
        Obtém uma matéria pelo ID.
        
        Args:
            materia_id (int): ID da matéria a ser obtida.

        Returns:
            Optional[Materias]: Matéria encontrada ou None se não encontrada.
        """

        return self.session.query(Materias).filter(Materias.id == materia_id).first()

    def obter_por_nome(self, nome: str) -> Optional[Materias]:
        """Obtém uma matéria pelo nome.
        
        Args:
            nome (str): Nome da matéria a ser obtida.

        Returns:
            Optional[Materias]: Matéria encontrada ou None se não encontrada.
        """

        return self.session.query(Materias).filter(Materias.nome == nome).first()

    def listar_todas(self) -> List[Materias]:
        """
        Lista todas as matérias.
        
        Returns:
            List[Materias]: Lista de todas as matérias cadastradas no sistema.
        """

        return self.session.query(Materias).all()

    def listar_por_professor(self, professor_id: int) -> List[Materias]:
        """
        Lista matérias de um professor.
        
        Returns:
            List[Materias]: Lista de matérias associadas ao professor especificado.
        """

        return self.session.query(Materias).filter(Materias.professor_id == professor_id).all()

    def atualizar(self, materia_id: int, **kwargs) -> Optional[Materias]:
        """
        Atualiza uma matéria existente.
        
        Args:
            materia_id (int): ID da matéria a ser atualizada.
            **kwargs: Campos a serem atualizados (ex: nome, professor_id).
            
        Returns:
            Optional[Materias]: Matéria atualizada ou None se a matéria não for encontrada.
        """

        materia = self.session.query(Materias).filter(Materias.id == materia_id).first()
        if materia:
            for key, value in kwargs.items():
                if hasattr(materia, key) and value is not None:
                    setattr(materia, key, value)
            self.session.commit()
            self.session.refresh(materia)
        return materia

    def deletar(self, materia_id: int) -> bool:
        """
        Deleta uma matéria.
        
        Args:
            materia_id (int): ID da matéria a ser deletada.
            
        Returns:
            bool: True se a matéria foi deletada, False se a matéria não foi encontrada.
        """

        materia = self.session.query(Materias).filter(Materias.id == materia_id).first()
        if materia:
            self.session.delete(materia)
            self.session.commit()
            return True
        return False