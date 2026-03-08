"""
Classe DAO com as operações de CRUD para a entidade Mutante, responsável por criar, obter, listar, atualizar e deletar 
mutantes no sistema.
"""

__author__ = "Davi Franco"

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models import Mutante
from typing import List, Optional

class MutanteDAO:
    def __init__(self, session: Session):
        self.session = session


    def criar(
        self, 
        matricula: str, 
        nome: str, 
        email: str, 
        senha: str, 
        esta_ativo: bool = False, 
        turma_id: Optional[int] = None
    ) -> Mutante:
        """
        Cria um novo mutante.
        
        Args:
            matricula (str): Matrícula do mutante.
            nome (str): Nome do mutante.
            email (str): Email do mutante.
            senha (str): Senha do mutante.
            esta_ativo (bool, optional): Indica se o mutante está ativo. Defaults para False.
            poder_id (Optional[int], optional): ID do poder associado ao mutante. Defaults para None.
            turma_id (Optional[int], optional): ID da turma associada ao mutante. Defaults para None.
        
        Returns:
            Mutante: O mutante criado no sistema.
        """

        novo_mutante = Mutante(
            matricula=matricula,
            nome=nome,
            email=email,
            senha=senha,
            esta_ativo=esta_ativo,
            turma_id=turma_id
        )
        self.session.add(novo_mutante)
        self.session.commit()
        self.session.refresh(novo_mutante)
        return novo_mutante


    def obter_por_id(self, mutante_id: int) -> Optional[Mutante]:
        """
        Obtém um mutante pelo ID.
        
        Args:
            mutante_id (int): ID do mutante a ser obtido.
            
        Returns:
            Optional[Mutante]: Mutante encontrado ou None se não encontrado.
        """

        return self.session.query(Mutante).filter(Mutante.id == mutante_id).first()


    def obter_por_email(self, email: str) -> Optional[Mutante]:
        """
        Obtém um mutante pelo email.
        
        Args:
            email (str): Email do mutante a ser obtido.
            
        Returns:
            Optional[Mutante]: Mutante encontrado ou None se não encontrado.
        """

        return self.session.query(Mutante).filter(Mutante.email == email).first()


    def obter_por_matricula(self, matricula: str) -> Optional[Mutante]:
        """
        Obtém um mutante pela matrícula.
        
        Args:
            matricula (str): Matrícula do mutante a ser obtido.
            
        Returns:
            Optional[Mutante]: Mutante encontrado ou None se não encontrado.
        """

        return self.session.query(Mutante).filter(Mutante.matricula == matricula).first()


    def obter_matricula_vazia(self, matricula: str) -> Optional[Mutante]:
        """
        Verifica se a matrícula passada como parâmetro tem o resto de suas credenciais vazias.
        
        Args:
            matricula (str): Matrícula do mutante a ser verificada.
        
        Returns:
            Optional[Mutante]: Mutante encontrado com a matrícula e credenciais vazias ou None se não encontrado.
        """

        return self.session.query(Mutante).filter(
            Mutante.matricula == matricula,
            or_(Mutante.nome == None, Mutante.nome == ""),
            or_(Mutante.email == None, Mutante.email == ""),
            or_(Mutante.senha == None, Mutante.senha == ""),
        ).first()


    def listar_todos(self) -> List[Mutante]:
        """Lista todos os mutantes."""

        return self.session.query(Mutante).all()


    def atualizar(self, mutante_id: int, **kwargs) -> Optional[Mutante]:
        """
        Atualiza um mutante.
        
        Args:
            mutante_id (int): ID do mutante a ser atualizado.
            **kwargs: Campos a serem atualizados (ex: nome, email, senha, poder_id, turma_id).
        
        Returns:
            Optional[Mutante]: Mutante atualizado ou None se não encontrado.
        """

        mutante = self.session.query(Mutante).filter(Mutante.id == mutante_id).first()
        
        if mutante:
            for key, value in kwargs.items():
                if hasattr(mutante, key) and value is not None:
                    setattr(mutante, key, value)

            self.session.commit()
            self.session.refresh(mutante)

        return mutante
    

    def deletar(self, mutante_id: int) -> bool:
        """
        Deleta um mutante.
        
        Args:
            mutante_id (int): ID do mutante a ser deletado.
            
        Returns:
            bool: True se o mutante foi deletado, False se o mutante não foi encontrado.
        """

        mutante = self.session.query(Mutante).filter(Mutante.id == mutante_id).first()
        if mutante:
            self.session.delete(mutante)
            self.session.commit()
            return True
        return False