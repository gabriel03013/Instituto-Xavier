"""
Service para gerenciar os poderes do Instituto. Este service é responsável por criar, listar, obter, atualizar e
deletar poderes. Ele utiliza o DAO de poderes para realizar as operações necessárias no banco de dados e retorna
os resultados como objetos de esquema apropriados.
"""

__author__ = "Davi Franco"

from src.dao.poder_dao import PoderDAO
from src.schemas.poderes_schema import PoderCreate, PoderUpdate, PoderSchema
from typing import List, Dict

class PoderService:
    def __init__(self, poder_dao: PoderDAO):
        self.poder_dao = poder_dao

    def criar_novo_poder(self, dados: PoderCreate) -> PoderSchema:
        """
        Verifica se já existe um poder com o mesmo nome, caso exista lança um ValueError. Caso contrário, cria um
        novo poder utilizando o DAO e retorna o poder criado como um objeto PoderSchema.

        Args:
            dados (PoderCreate): Dados necessários para criar um novo poder.

        Raises:
            ValueError: Se o poder já existir.

        Returns:
            PoderSchema: O poder criado como um objeto PoderSchema.
        """
        if self.poder_dao.obter_por_nome(dados.nome):
            raise ValueError(f"Poder '{dados.nome}' já existe")

        poder = self.poder_dao.criar(nome=dados.nome)

        return PoderSchema.model_validate(poder)

    def listar_poderes(self) -> List[PoderSchema]:
        """
        Lista todos os poderes utilizando o DAO e retorna uma lista de objetos PoderSchema.

        Returns:
            List[PoderSchema]: Uma lista de objetos PoderSchema representando todos os poderes.
        """
        poderes = self.poder_dao.listar_todos()
        return [PoderSchema.model_validate(p) for p in poderes]

    def obter_poder_por_id(self, poder_id: int) -> PoderSchema:
        """
        Obtém um poder por ID utilizando o DAO. Se o poder não for encontrado, lança um ValueError. Caso contrário,
        retorna o poder encontrado como um objeto PoderSchema.

        Args:
            poder_id (int): O ID do poder a ser obtido.

        Raises:
            ValueError: Se o poder não for encontrado.

        Returns:
            PoderSchema: O poder encontrado como um objeto PoderSchema.
        """
        poder = self.poder_dao.obter_por_id(poder_id)
        if not poder:
            raise ValueError(f"Poder {poder_id} não encontrado")

        return PoderSchema.model_validate(poder)

    def atualizar_poder(self, poder_id: int, dados: PoderUpdate) -> PoderSchema:
        """
        Verifica se o poder existe utilizando o DAO. Se o poder não for encontrado, lança um ValueError. Caso contrário,
        verifica se o campo "nome" está presente nos dados de atualização e se já existe um poder com o mesmo nome
        (excluindo o poder atual). Se existir, lança um ValueError. Caso contrário, atualiza o poder utilizando o DAO
        e retorna o poder atualizado como um objeto PoderSchema.

        Args:
            poder_id (int): O ID do poder a ser atualizado.
            dados (PoderUpdate): Dados de atualização para o poder.

        Raises:
            ValueError: Se o poder não for encontrado.
            ValueError: Se já existir um poder com o mesmo nome.

        Returns:
            PoderSchema: O poder atualizado como um objeto PoderSchema.
        """
        poder = self.poder_dao.obter_por_id(poder_id)
        if not poder:
            raise ValueError(f"Poder {poder_id} não encontrado")

        dados_dict = dados.model_dump(exclude_unset=True)

        if 'nome' in dados_dict and dados_dict['nome']:
            nome_existe = self.poder_dao.obter_por_nome(dados_dict['nome'])
            if nome_existe and nome_existe.id != poder_id:
                raise ValueError(f"Poder '{dados_dict['nome']}' já existe")

        poder_atualizado = self.poder_dao.atualizar(poder_id, **dados_dict)

        return PoderSchema.model_validate(poder_atualizado)

    def deletar_poder(self, poder_id: int) -> Dict:
        """
        Verifica se o poder existe utilizando o DAO. Se o poder não for encontrado, lança um ValueError. Caso contrário,
        deleta o poder utilizando o DAO e retorna um dicionário contendo o ID do poder deletado e um indicador de que
        o poder foi deletado.

        Args:
            poder_id (int): O ID do poder a ser deletado.

        Raises:
            ValueError: Se o poder não for encontrado.

        Returns:
            Dict: Com os dados do poder deletado.
        """
        poder = self.poder_dao.obter_por_id(poder_id)
        if not poder:
            raise ValueError(f"Poder {poder_id} não encontrado")

        self.poder_dao.deletar(poder_id)

        return {
            "id": poder_id,
            "deletado": True
        }