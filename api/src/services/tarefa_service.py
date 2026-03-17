"""
Service para gerenciar as tarefas criadas pelos mutantes. Este service é responsável
por criar, listar, obter, atualizar, concluir e deletar tarefas. Ele utiliza o DAO
de tarefas para realizar operações no banco e retorna os resultados como schemas.
"""

__author__ = "Erik Santos"

from dao.tarefa_dao import TarefaDAO
from schemas.tarefas_schema import (
    TarefaCreate,
    TarefaUpdate,
    TarefaResponse,
    TarefaSchema
)
from typing import List, Dict
from datetime import datetime


class TarefaService:
    def __init__(self, tarefa_dao: TarefaDAO):
        self.tarefa_dao = tarefa_dao


    def criar_tarefa(self, dados: TarefaCreate) -> TarefaResponse:
        """
        Cria uma nova tarefa.

        Args:
            dados (TarefaCreate): Dados da tarefa.

        Returns:
            TarefaResponse: Tarefa criada.
        """
        tarefa = self.tarefa_dao.criar(
            titulo=dados.titulo,
            descricao=dados.descricao,
            status="Pendente",
            prioridade=dados.prioridade,
            data_criacao=datetime.utcnow(),
            data_limite=dados.data_limite,
            mutante_id=dados.mutante_id
        )

        return TarefaResponse.model_validate(tarefa)


    def listar_tarefas(self) -> List[TarefaSchema]:
        """
        Lista todas as tarefas.

        Returns:
            List[TarefaSchema]
        """
        tarefas = self.tarefa_dao.listar_todos()
        return [TarefaSchema.model_validate(t) for t in tarefas]


    def listar_tarefas_por_mutante(self, mutante_id: int) -> List[TarefaSchema]:
        """
        Lista tarefas de um mutante específico.

        Args:
            mutante_id (int): ID do mutante.

        Returns:
            List[TarefaSchema]: Lista de tarefas do mutante.
        """
        tarefas = self.tarefa_dao.listar_por_mutante(mutante_id)

        return [TarefaSchema.model_validate(t) for t in tarefas]

    
    def listar_tarefas_por_status(self, status: str) -> List[TarefaSchema]:
        """
        Lista tarefas filtradas pelo status.

        Args:
            status (str): Status da tarefa.

        Returns:
            List[TarefaSchema]: Lista de tarefas filtradas.
        """
        tarefas = self.tarefa_dao.listar_por_status(status)

        return [TarefaSchema.model_validate(t) for t in tarefas]


    def obter_tarefa_por_id(self, tarefa_id: int) -> TarefaSchema:
        """
        Obtém uma tarefa pelo ID.

        Raises:
            ValueError: Se a tarefa não existir.
        """
        tarefa = self.tarefa_dao.obter_por_id(tarefa_id)

        if not tarefa:
            raise ValueError(f"Tarefa {tarefa_id} não encontrada")

        return TarefaSchema.model_validate(tarefa)


    def atualizar_tarefa(self, tarefa_id: int, dados: TarefaUpdate) -> TarefaSchema:
        """
        Atualiza uma tarefa existente.

        Args:
            tarefa_id (int)
            dados (TarefaUpdate)

        Raises:
            ValueError: Se a tarefa não existir.
        """
        tarefa = self.tarefa_dao.obter_por_id(tarefa_id)

        if not tarefa:
            raise ValueError(f"Tarefa {tarefa_id} não encontrada")

        dados_dict = dados.model_dump(exclude_unset=True)

        tarefa_atualizada = self.tarefa_dao.atualizar(
            tarefa_id,
            **dados_dict
        )

        return TarefaSchema.model_validate(tarefa_atualizada)


    def concluir_tarefa(self, tarefa_id: int) -> TarefaResponse:
        """
        Marca uma tarefa como concluída.

        Raises:
            ValueError: Se a tarefa não existir ou já estiver concluída.
        """
        tarefa = self.tarefa_dao.obter_por_id(tarefa_id)

        if not tarefa:
            raise ValueError(f"Tarefa {tarefa_id} não encontrada")

        if tarefa.status == "Concluída":
            raise ValueError("Tarefa já está concluída")

        tarefa_concluida = self.tarefa_dao.atualizar(
            tarefa_id,
            status="Concluída",
            data_conclusao=datetime.utcnow()
        )

        return TarefaResponse.model_validate(tarefa_concluida)


    def deletar_tarefa(self, tarefa_id: int) -> Dict:
        """
        Deleta uma tarefa.

        Raises:
            ValueError: Se a tarefa não existir.
        """
        tarefa = self.tarefa_dao.obter_por_id(tarefa_id)

        if not tarefa:
            raise ValueError(f"Tarefa {tarefa_id} não encontrada")

        self.tarefa_dao.deletar(tarefa_id)

        return {
            "id": tarefa_id,
            "deletado": True
        }