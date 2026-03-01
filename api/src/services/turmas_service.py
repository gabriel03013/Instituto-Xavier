"""
Service para gerenciar as turmas do Instituto. Este service é responsável por criar, listar, obter, atualizar e 
deletar turmas, além de lidar com a associação entre mutantes e turmas. Ele utiliza os DAOs de turmas e mutantes para 
realizar as operações necessárias no banco de dados e retorna os resultados como objetos de esquema apropriados.
"""

__author__ = "Davi Franco"

from src.dao.turmas_dao import TurmasDAO
from src.dao.mutante_dao import MutanteDAO
from src.schemas.turmas_schema import TurmaCreate, TurmaUpdate, TurmaSchema
from typing import List, Dict

class TurmasService:
    def __init__(self, turmas_dao: TurmasDAO, mutante_dao: MutanteDAO):
        self.turmas_dao = turmas_dao
        self.mutante_dao = mutante_dao

    def criar_nova_turma(self, dados: TurmaCreate) -> TurmaSchema:
        """
            Verifica se já existe uma turma com a mesma série e turma, caso exista lança um ValueError. Caso contrário, cria uma
            nova turma utilizando o DAO e retorna a turma criada como um objeto TurmaSchema.

        Args:
            dados (TurmaCreate): 

        Raises:
            ValueError: Se a turma já existir.

        Returns:
            TurmaSchema: A turma criada como um objeto TurmaSchema.
        """
        
        
        turma_existe = self.turmas_dao.obter_por_serie_e_turma(dados.serie, dados.turma)
        if turma_existe:
            raise ValueError(f"Turma {dados.serie}{dados.turma} já existe")

        nova_turma = self.turmas_dao.criar(serie=dados.serie, turma=dados.turma)

        return TurmaSchema.model_validate(nova_turma)

    def listar_turmas(self) -> List[TurmaSchema]:
        """
            Lista todas as turmas utilizando o DAO e retorna uma lista de objetos TurmaSchema.        

        Returns:
            List[TurmaSchema]: Uma lista de objetos TurmaSchema representando todas as turmas.
        """
        
        turmas = self.turmas_dao.listar_todas()
        return [TurmaSchema.model_validate(t) for t in turmas]

    def obter_turma_por_id(self, turma_id: int) -> TurmaSchema:
        """
            Obtém uma turma por ID utilizando o DAO. Se a turma não for encontrada, lança um ValueError. Caso contrário, 
            retorna a turma encontrada como um objeto TurmaSchema.

        Args:
            turma_id (int): _description_

        Raises:
            ValueError: _description_

        Returns:
            TurmaSchema: _description_
        """
        
        turma = self.turmas_dao.obter_por_id(turma_id)
        if not turma:
            raise ValueError(f"Turma {turma_id} não encontrada")

        return TurmaSchema.model_validate(turma)

    def listar_turmas_por_serie(self, serie: int) -> List[TurmaSchema]:
        """
            Lista as turmas por série utilizando o DAO e retorna uma lista de objetos TurmaSchema. Se não houver turmas para 
            a série

        Args:
            serie (int): _description_

        Returns:
            List[TurmaSchema]: _description_
        """
        
        turmas = self.turmas_dao.listar_por_serie(serie)
        return [TurmaSchema.model_validate(t) for t in turmas]

    def atualizar_turma(self, turma_id: int, dados: TurmaUpdate) -> TurmaSchema:
        """
            Verifica se a turma existe utilizando o DAO. Se a turma não for encontrada, lança um ValueError. Caso contrário, 
            verifica se os campos "serie" e "turma" estão presentes nos dados de atualização e se já existe uma turma com a 
            mesma série e turma (excluindo a turma atual). Se existir, lança um ValueError. Caso contrário, atualiza a turma
            utilizando o DAO e retorna a turma atualizada como um objeto TurmaSchema.

        Args:
            turma_id (int): para identificar a turma a ser atualizada.
            dados (TurmaUpdate): dados de atualização para a turma.

        Raises:
            ValueError: Se a turma não for encontrada.
            ValueError: Se já existir uma turma com a mesma série e turma.

        Returns:
            TurmaSchema: A turma atualizada como um objeto TurmaSchema.
        """
        
        turma = self.turmas_dao.obter_por_id(turma_id)
        if not turma:
            raise ValueError(f"Turma {turma_id} não encontrada")

        dados_dict = dados.model_dump(exclude_unset=True)

        if 'serie' in dados_dict and 'turma' in dados_dict:
            turma_existe = self.turmas_dao.obter_por_serie_e_turma(
                dados_dict['serie'],
                dados_dict['turma']
            )
            if turma_existe and turma_existe.id != turma_id:
                raise ValueError(f"Turma {dados_dict['serie']}{dados_dict['turma']} já existe")

        turma_atualizada = self.turmas_dao.atualizar(turma_id, **dados_dict)

        return TurmaSchema.model_validate(turma_atualizada)

    def deletar_turma(self, turma_id: int) -> Dict:
        """
            Verifica se a turma existe utilizando o DAO. Se a turma não for encontrada, lança um ValueError. Caso contrário,
            lista todos os mutantes utilizando o DAO e filtra os mutantes que pertencem à turma a ser deletada. Para cada 
            mutante pertencente à turma, atualiza o campo "turma_id" para None utilizando o DAO. Por fim, deleta a turma 
            utilizando o DAO e retorna um dicionário contendo o ID da turma deletada, um indicador de que a turma foi 
            deletada e a quantidade de alunos que foram atualizados.

        Args:
            turma_id (int): para indentificar a turma a ser deletada.

        Raises:
            ValueError: caso a turma não seja encontrada.

        Returns:
            Dict: com os dados da turma deletada e a quantidade de alunos atualizados.
        """
        
        turma = self.turmas_dao.obter_por_id(turma_id)
        if not turma:
            raise ValueError(f"Turma {turma_id} não encontrada")

        mutantes = self.mutante_dao.listar_todos()
        alunos_turma = [m for m in mutantes if m.turma_id == turma_id]

        for aluno in alunos_turma:
            self.mutante_dao.atualizar(aluno.id, turma_id=None)

        self.turmas_dao.deletar(turma_id)

        return {
            "id": turma_id,
            "deletado": True,
            "alunos_atualizados": len(alunos_turma)
        }