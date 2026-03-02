from dao.professor_dao import ProfessorDAO
from dao.materias_dao import MateriasDAO
from schemas.professores_schema import ProfessorCreate, ProfessorUpdate, ProfessorSchema
"""
Service para gerenciar os professores do Instituto. Este service é responsável por criar, listar, obter, atualizar e 
deletar professores, além de lidar com a exclusão das matérias associadas. Ele utiliza os DAOs de professores e matérias 
para realizar as operações necessárias no banco de dados e retorna os resultados como objetos de esquema apropriados.
"""

__author__ = "Davi Franco"


from typing import List, Dict

class ProfessorService:
    def __init__(self, professor_dao: ProfessorDAO, materias_dao: MateriasDAO):
        self.professor_dao = professor_dao
        self.materias_dao = materias_dao
        

    def criar_novo_professor(self, dados: ProfessorCreate) -> ProfessorSchema:
        """
        Verifica se já existe um professor com o mesmo usuário, caso exista lança um ValueError. Caso contrário, cria um
        novo professor utilizando o DAO e retorna o professor criado como um objeto ProfessorSchema.

        Args:
            dados (ProfessorCreate): Dados necessários para criar um novo professor.

        Raises:
            ValueError: Se o usuário já existir.

        Returns:
            ProfessorSchema: O professor criado como um objeto ProfessorSchema.
        """
        if self.professor_dao.obter_por_usuario(dados.usuario):
            raise ValueError(f"Usuário '{dados.usuario}' já existe")

        professor = self.professor_dao.criar(
            nome=dados.nome,
            usuario=dados.usuario,
            senha=dados.senha
        )

        return ProfessorSchema.model_validate(professor)

    def listar_professores(self) -> List[ProfessorSchema]:
        """
        Lista todos os professores utilizando o DAO e retorna uma lista de objetos ProfessorSchema.

        Returns:
            List[ProfessorSchema]: Uma lista de objetos ProfessorSchema representando todos os professores.
        """
        professores = self.professor_dao.listar_todos()
        return [ProfessorSchema.model_validate(p) for p in professores]

    def obter_professor_por_id(self, professor_id: int) -> ProfessorSchema:
        """
        Obtém um professor por ID utilizando o DAO. Se o professor não for encontrado, lança um ValueError. Caso contrário,
        retorna o professor encontrado como um objeto ProfessorSchema.

        Args:
            professor_id (int): O ID do professor a ser obtido.

        Raises:
            ValueError: Se o professor não for encontrado.

        Returns:
            ProfessorSchema: O professor encontrado como um objeto ProfessorSchema.
        """
        professor = self.professor_dao.obter_por_id(professor_id)
        if not professor:
            raise ValueError(f"Professor {professor_id} não encontrado")

        return ProfessorSchema.model_validate(professor)

    def atualizar_professor(self, professor_id: int, dados: ProfessorUpdate) -> ProfessorSchema:
        """
        Verifica se o professor existe utilizando o DAO. Se o professor não for encontrado, lança um ValueError. Caso contrário,
        verifica se o campo "usuario" está presente nos dados de atualização e se já existe um professor com o mesmo usuário
        (excluindo o professor atual). Se existir, lança um ValueError. Caso contrário, atualiza o professor utilizando o DAO
        e retorna o professor atualizado como um objeto ProfessorSchema.

        Args:
            professor_id (int): O ID do professor a ser atualizado.
            dados (ProfessorUpdate): Dados de atualização para o professor.

        Raises:
            ValueError: Se o professor não for encontrado.
            ValueError: Se já existir um professor com o mesmo usuário.

        Returns:
            ProfessorSchema: O professor atualizado como um objeto ProfessorSchema.
        """
        professor = self.professor_dao.obter_por_id(professor_id)
        if not professor:
            raise ValueError(f"Professor {professor_id} não encontrado")

        dados_dict = dados.model_dump(exclude_unset=True)

        if 'usuario' in dados_dict and dados_dict['usuario']:
            usuario_existe = self.professor_dao.obter_por_usuario(dados_dict['usuario'])
            if usuario_existe and usuario_existe.id != professor_id:
                raise ValueError(f"Usuário '{dados_dict['usuario']}' já existe")

        professor_atualizado = self.professor_dao.atualizar(professor_id, **dados_dict)

        return ProfessorSchema.model_validate(professor_atualizado)

    def deletar_professor(self, professor_id: int) -> Dict:
        """
        Verifica se o professor existe utilizando o DAO. Se o professor não for encontrado, lança um ValueError. Caso contrário,
        lista todas as matérias associadas ao professor utilizando o DAO e deleta cada uma delas. Por fim, deleta o professor
        utilizando o DAO e retorna um dicionário contendo o ID do professor deletado, um indicador de que o professor foi
        deletado e a quantidade de matérias que foram removidas.

        Args:
            professor_id (int): O ID do professor a ser deletado.

        Raises:
            ValueError: Se o professor não for encontrado.

        Returns:
            Dict: Com os dados do professor deletado e a quantidade de matérias removidas.
        """
        professor = self.professor_dao.obter_por_id(professor_id)
        if not professor:
            raise ValueError(f"Professor {professor_id} não encontrado")

        materias = self.materias_dao.listar_por_professor(professor_id)
        for materia in materias:
            self.materias_dao.deletar(materia.id)

        self.professor_dao.deletar(professor_id)

        return {
            "id": professor_id,
            "deletado": True,
            "materias_removidas": len(materias)
        }