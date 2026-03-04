"""
Classe DAO para a entidade MutantesMaterias, responsável por realizar as operações de CRUD (Create, Read, Update, Delete)
"""

__author__ = "Davi Franco"

from sqlalchemy.orm import Session
from api.src.models import MutantesMaterias, Mutante
from typing import List, Optional

class MutantesMateriasDAO:
    def __init__(self, session: Session):
        self.session = session

    def criar(self, mutante_id: int, materia_id: int, 
              nota1: Optional[int] = None, nota2: Optional[int] = None) -> MutantesMaterias:
        """
        Cria um registro mutante-matéria.
        
        Args:
            mutante_id (int): ID do mutante.
            materia_id (int): ID da matéria.
            nota1 (Optional[int], optional): Nota 1 do mutante na matéria. Defaults para None.
            nota2 (Optional[int], optional): Nota 2 do mutante na matéria. Defaults para None.
            
        Returns:
            MutantesMaterias: O registro criado no sistema.
        """

        novo_registro = MutantesMaterias(
            mutante_id=mutante_id,
            materia_id=materia_id,
            nota1=nota1,
            nota2=nota2
        )
        self.session.add(novo_registro)
        self.session.commit()
        self.session.refresh(novo_registro)
        return novo_registro

    def obter_por_id(self, registro_id: int) -> Optional[MutantesMaterias]:
        """
        Obtém um registro pelo ID.
        
        Args:
            registro_id (int): ID do registro a ser obtido.
            
        Returns:
            Optional[MutantesMaterias]: Registro encontrado ou None se não encontrado.
        """

        return self.session.query(MutantesMaterias).filter(MutantesMaterias.id == registro_id).first()

    def obter_por_mutante_e_materia(self, mutante_id: int, 
                                     materia_id: int) -> Optional[MutantesMaterias]:
        """
        Obtém registro de mutante e matéria.
        
        Args:
            mutante_id (int): ID do mutante.
            materia_id (int): ID da matéria.
            
        Returns:
            Optional[MutantesMaterias]: Registro encontrado ou None se não encontrado.
        """

        return self.session.query(MutantesMaterias).filter(
            (MutantesMaterias.mutante_id == mutante_id) &
            (MutantesMaterias.materia_id == materia_id)
        ).first()

    def listar_por_mutante(self, mutante_id: int) -> List[MutantesMaterias]:
        """
        Lista matérias de um mutante.
        
        Args:
            mutante_id (int): ID do mutante.
            
        Returns:
            List[MutantesMaterias]: Lista de registros do mutante em suas matérias.
        """

        return self.session.query(MutantesMaterias).filter(MutantesMaterias.mutante_id == mutante_id).all()

    def listar_por_materia(self, materia_id: int) -> List[MutantesMaterias]:
        """
        Lista mutantes de uma matéria.
        
        Args:
            materia_id (int): ID da matéria.
        
        Returns:
            List[MutantesMaterias]: Lista de registros da matéria com os mutantes matriculados.
        """

        return self.session.query(MutantesMaterias).filter(MutantesMaterias.materia_id == materia_id).all()

    def listar_por_turma_e_materia(self, turma_id: int, materia_id: int) -> List[MutantesMaterias]:
        """
        Lista mutantes de uma turma em uma determinada matéria.
        
        Args:
            turma_id (int): ID da turma.
            materia_id (int): ID da matéria.
            
        Returns:
            List[MutantesMaterias]: Lista de registros dos mutantes da turma em uma matéria específica.
        """
        
        return self.session.query(MutantesMaterias).join(Mutante).filter(
            (Mutante.turma_id == turma_id) &
            (MutantesMaterias.materia_id == materia_id)
        ).all()

    def listar_todos(self) -> List[MutantesMaterias]:
        """Lista todos os registros."""

        return self.session.query(MutantesMaterias).all()

    def atualizar_notas(self, registro_id: int, nota1: Optional[int] = None, 
                        nota2: Optional[int] = None) -> Optional[MutantesMaterias]:
        """
        Atualiza as notas de um registro.
        
        Args:
            registro_id (int): ID do registro a ser atualizado.
            nota1 (Optional[int]): Nova nota1 do registro.
            nota2 (Optional[int]): Nova nota2 do registro.
            
        Returns:
            Optional[MutantesMaterias]: Registro atualizado ou None se não encontrado.
        """

        registro = self.session.query(MutantesMaterias).filter(MutantesMaterias.id == registro_id).first()
        if registro:
            if nota1 is not None:
                registro.nota1 = nota1
            if nota2 is not None:
                registro.nota2 = nota2
            self.session.commit()
            self.session.refresh(registro)
        return registro

    def deletar(self, registro_id: int) -> bool:
        """
        Deleta um registro.
        
        Args:
            registro_id (int): ID do registro a ser deletado.
            
        Returns:
            bool: True se o registro foi deletado, False se o registro não foi encontrado.
        """

        registro = self.session.query(MutantesMaterias).filter(MutantesMaterias.id == registro_id).first()
        if registro:
            self.session.delete(registro)
            self.session.commit()
            return True
        return False