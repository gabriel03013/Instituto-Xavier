"""
Classe DAO com as operações de CRUD para a entidade Tarefa, responsável por criar, obter, listar, atualizar e deletar 
tarefas que o mutante cria no sistema.
"""

__author__ = "Erik Santos"

from sqlalchemy.orm import Session
from typing import List, Optional
from models import Tarefa
from datetime import datetime


class TarefaDAO:
    def __init__(self, session: Session):
        self.session = session


    def criar(
        self,
        titulo: str,
        mutante_id: int,
        descricao: Optional[str] = None,
        status: str = "Pendente",
        prioridade: Optional[str] = None,
        data_limite=None
    ) -> Tarefa:
        """
        Cria uma nova tarefa.

        Args:
            titulo (str): Título da tarefa.
            mutante_id (int): ID do mutante dono da tarefa.
            descricao (Optional[str]): Descrição da tarefa.
            status (str): Status da tarefa.
            prioridade (Optional[str]): Prioridade da tarefa.
            data_limite (Optional[datetime]): Data limite da tarefa.

        Returns:
            Tarefa: A tarefa criada.
        """
        nova_tarefa = Tarefa(
            titulo=titulo,
            descricao=descricao,
            status=status,
            prioridade=prioridade,
            data_limite=data_limite,
            mutante_id=mutante_id
        )

        self.session.add(nova_tarefa)
        self.session.commit()
        self.session.refresh(nova_tarefa)

        return nova_tarefa


    def obter_por_id(self, tarefa_id: int) -> Optional[Tarefa]:
        """
        Obtém uma tarefa pelo ID.
        """
        return self.session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()


    def listar_todos(self) -> List[Tarefa]:
        """
        Lista todas as tarefas.
        """
        return self.session.query(Tarefa).all()


    def listar_por_mutante(self, mutante_id: int) -> List[Tarefa]:
        """
        Lista todas as tarefas de um mutante.
        """
        return self.session.query(Tarefa).filter(Tarefa.mutante_id == mutante_id).all()


    def atualizar(self, tarefa_id: int, **kwargs) -> Optional[Tarefa]:
        """
        Atualiza uma tarefa.

        Args:
            tarefa_id (int): ID da tarefa.
            **kwargs: Campos para atualização.

        Returns:
            Optional[Tarefa]: Tarefa atualizada ou None.
        """
        tarefa = self.session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()

        if tarefa:
            for key, value in kwargs.items():
                if hasattr(tarefa, key) and value is not None:
                    setattr(tarefa, key, value)

            self.session.commit()
            self.session.refresh(tarefa)

        return tarefa


    def deletar(self, tarefa_id: int) -> bool:
        """
        Deleta uma tarefa.
        """
        tarefa = self.session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()

        if tarefa:
            self.session.delete(tarefa)
            self.session.commit()
            return True

        return False


    def concluir_tarefa(self, tarefa_id: int, mutante_id: int) -> Optional[Tarefa]:
        """
        Marca uma tarefa como concluída garantindo que pertence ao mutante.
        """
        tarefa = self.session.query(Tarefa).filter(
            Tarefa.id == tarefa_id,
            Tarefa.mutante_id == mutante_id
        ).first()

        if tarefa:
            tarefa.status = "Concluída"
            tarefa.data_conclusao = datetime.utcnow()

            self.session.commit()
            self.session.refresh(tarefa)

        return tarefa
