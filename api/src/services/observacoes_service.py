"""
Service para gerenciar as turmas do Instituto. Este service é responsável por criar, listar, obter, atualizar e 
deletar turmas, além de lidar com a associação entre mutantes e turmas. Ele utiliza os DAOs de turmas e mutantes para 
realizar as operações necessárias no banco de dados e retorna os resultados como objetos de esquema apropriados.
"""

__author__ = "Davi Franco"

from dao.observacoes_dao import ObservacoesDAO
from dao.mutantes_materias_dao import MutantesMateriasDAO
from schemas.observacoes_schema import ObservacaoCreate, ObservacaoUpdate, ObservacaoSchema, ObservacaoStudentSchema
from typing import List, Dict
from datetime import date

class ObservacoesService:
    def __init__(self, observacoes_dao: ObservacoesDAO, mutantes_materias_dao: MutantesMateriasDAO):
        self.observacoes_dao = observacoes_dao
        self.mutantes_materias_dao = mutantes_materias_dao

    def adicionar_observacao(self, dados: ObservacaoCreate) -> ObservacaoSchema:
        """
            Adiciona uma nova observação para um registro mutante-matéria específico. O método verifica se o registro 
            mutante-matéria existe e se a observação não está vazia antes de criar a nova observação no banco de dados. 
            Se o registro mutante-matéria não for encontrado ou se a observação estiver vazia, ele lança um ValueError com 
            uma mensagem apropriada. Caso contrário, ele retorna a nova observação criada como um objeto ObservacaoSchema.

        Args:
            dados (ObservacaoCreate): Dados necessários para criar uma nova observação, incluindo o ID do registro 
            mutante-matéria, a observação em si e a data da observação.

        Raises:
            ValueError: caso o registro mutante-matéria não exista.
            ValueError: caso a observação esteja vazia.
        Returns:
            ObservacaoSchema: O objeto ObservacaoSchema representando a nova observação criada.
        """
        
        if not self.mutantes_materias_dao.obter_por_id(dados.mutantesmaterias_id):
            raise ValueError(f"Registro mutante-matéria {dados.mutantesmaterias_id} não encontrado")

        if not dados.observacao or len(dados.observacao.strip()) == 0:
            raise ValueError("Observação não pode estar vazia")

        obs = self.observacoes_dao.criar(
            mutantesmaterias_id=dados.mutantesmaterias_id,
            observacao=dados.observacao,
            data=dados.data
        )

        return ObservacaoSchema.model_validate(obs)

    def listar_observacoes_registro(self, mutantesmaterias_id: int) -> List[ObservacaoSchema]:
        """
            Lista todas as observações associadas a um registro mutante-matéria específico.

        Args:
            mutantesmaterias_id (int): ID do registro mutante-matéria para o qual se deseja listar as observações.

        Raises:
            ValueError: caso o registro mutante-matéria não exista.

        Returns:
            List[ObservacaoSchema]: Lista de objetos ObservacaoSchema representando as observações associadas ao registro.
        """
        
        if not self.mutantes_materias_dao.obter_por_id(mutantesmaterias_id):
            raise ValueError(f"Registro mutante-matéria {mutantesmaterias_id} não encontrado")

        observacoes = self.observacoes_dao.listar_por_mutante_materia(mutantesmaterias_id)
        return [ObservacaoSchema.model_validate(o) for o in observacoes]

    def listar_observacoes_periodo(self, data_inicio: date, data_fim: date) -> List[ObservacaoSchema]:
        """
            Lista as observações feitas em um período específico, definido por uma data de início e uma data de fim. 
            O método utiliza o DAO para buscar as observações dentro do intervalo de datas fornecido e retorna as observações 
            encontradas como uma lista de objetos ObservacaoSchema.

        Args:
            data_inicio (date): Data de início do período.
            data_fim (date): Data de fim do período.

        Returns:
            List[ObservacaoSchema]: lista de objetos ObservacaoSchema representando as observações feitas no período especificado.
        """
        
        
        observacoes = self.observacoes_dao.listar_por_data(data_inicio, data_fim)
        return [ObservacaoSchema.model_validate(o) for o in observacoes]

    def listar_todas_observacoes(self) -> List[ObservacaoSchema]:
        """
            Lista todas as observações no banco de dados utilizando o DAO e retorna uma lista de objetos ObservacaoSchema.

        Returns:
            List[ObservacaoSchema]: Lista de todos os objetos ObservacaoSchema no banco de dados.
        """
        
        
        observacoes = self.observacoes_dao.listar_todas()
        return [ObservacaoSchema.model_validate(o) for o in observacoes]

    def listar_observacoes_por_turma(self, turma_id: int) -> List[ObservacaoSchema]:
        """
            Lista todas as observações associadas aos mutantes de uma turma específica.

        Args:
            turma_id (int): ID da turma para a qual se deseja listar as observações.

        Returns:
            List[ObservacaoSchema]: Lista de objetos ObservacaoSchema representando as observações da turma.
        """
        observacoes = self.observacoes_dao.listar_por_turma(turma_id)
        return [ObservacaoSchema.model_validate(o) for o in observacoes]

    def listar_observacoes_por_mutante(self, mutante_id: int) -> List[ObservacaoStudentSchema]:
        """
            Lista todas as observações associadas a um mutante específico.

        Args:
            mutante_id (int): ID do mutante para o qual se deseja listar as observações.

        Returns:
            List[ObservacaoStudentSchema]: Lista de objetos ObservacaoStudentSchema representando as observações do mutante.
        """
        observacoes = self.observacoes_dao.listar_por_mutante(mutante_id)
        return [ObservacaoStudentSchema.model_validate(o) for o in observacoes]

    def obter_observacao_por_id(self, observacao_id: int) -> ObservacaoSchema:
        """
            Obtém uma observação por ID utilizando o DAO. Se a observação não for encontrada, lança um ValueError. Caso contrário,

        Args:
            observacao_id (int): ID da observação a ser obtida.

        Raises:
            ValueError: caso a observação não seja encontrada.

        Returns:
            ObservacaoSchema: O objeto ObservacaoSchema representando a observação encontrada.
        """
        
        
        obs = self.observacoes_dao.obter_por_id(observacao_id)
        if not obs:
            raise ValueError(f"Observação {observacao_id} não encontrada")

        return ObservacaoSchema.model_validate(obs)

    def atualizar_observacao(self, observacao_id: int, dados: ObservacaoUpdate) -> ObservacaoSchema:
        """
            Atualiza uma observação existente no banco de dados.

        Args:
            observacao_id (int): ID da observação a ser atualizada.
            dados (ObservacaoUpdate): Dados atualizados da observação.


        Raises:
            ValueError: caso a observação não seja encontrada.
            ValueError: caso a observação esteja vazia.

        Returns:
            ObservacaoSchema: O objeto ObservacaoSchema representando a observação atualizada.
        """
        
        
        obs = self.observacoes_dao.obter_por_id(observacao_id)
        if not obs:
            raise ValueError(f"Observação {observacao_id} não encontrada")

        dados_dict = dados.model_dump(exclude_unset=True)

        if 'observacao' in dados_dict and dados_dict['observacao']:
            if not dados_dict['observacao'].strip():
                raise ValueError("Observação não pode estar vazia")

        obs_atualizada = self.observacoes_dao.atualizar(observacao_id, **dados_dict)

        return ObservacaoSchema.model_validate(obs_atualizada)

    def deletar_observacao(self, observacao_id: int) -> Dict:
        """
            Deleta uma observação por ID utilizando o DAO. Se a observação não for encontrada, lança um ValueError. Caso contrário,

        Args:
            observacao_id (int): ID da observação a ser deletada.

        Raises:
            ValueError: caso a observação não seja encontrada.

        Returns:
            Dict: Dicionário contendo o ID da observação deletada e um indicador de sucesso.
        """
        
        
        obs = self.observacoes_dao.obter_por_id(observacao_id)
        if not obs:
            raise ValueError(f"Observação {observacao_id} não encontrada")

        self.observacoes_dao.deletar(observacao_id)

        return {
            "id": observacao_id,
            "deletado": True
        }