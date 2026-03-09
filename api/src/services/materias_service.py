"""
Service para gerenciar as matérias do Instituto. Este service é responsável por criar, listar, obter, atualizar e
deletar matérias, além de lidar com a exclusão das associações entre mutantes e matérias. Também fornece funcionalidades
para listar matérias por professor e gerar relatórios de desempenho. Ele utiliza os DAOs de matérias, professores e
mutantes-matérias para realizar as operações necessárias no banco de dados e retorna os resultados como objetos de
esquema apropriados.
"""

__author__ = "Davi Franco"

from dao.materias_dao import MateriasDAO
from dao.professor_dao import ProfessorDAO
from dao.mutantes_materias_dao import MutantesMateriasDAO
from schemas.materias_schema import MateriaCreate, MateriaUpdate, MateriaSchema
from typing import List, Dict

class MateriasService:
    def __init__(
        self,
        materias_dao: MateriasDAO,
        professor_dao: ProfessorDAO,
        mutantes_materias_dao: MutantesMateriasDAO
    ):
        self.materias_dao = materias_dao
        self.professor_dao = professor_dao
        self.mutantes_materias_dao = mutantes_materias_dao

    def criar_nova_materia(self, dados: MateriaCreate) -> MateriaSchema:
        """
        Verifica se já existe uma matéria com o mesmo nome, caso exista lança um ValueError. Em seguida, verifica se
        o professor fornecido existe, caso não exista lança um ValueError. Caso contrário, cria uma nova matéria
        utilizando o DAO e retorna a matéria criada como um objeto MateriaSchema.

        Args:
            dados (MateriaCreate): Dados necessários para criar uma nova matéria.

        Raises:
            ValueError: Se a matéria já existir.
            ValueError: Se o professor_id fornecido não existir.

        Returns:
            MateriaSchema: A matéria criada como um objeto MateriaSchema.
        """
        if self.materias_dao.obter_por_nome(dados.nome):
            raise ValueError(f"Matéria '{dados.nome}' já existe")

        if not self.professor_dao.obter_por_id(dados.professor_id):
            raise ValueError(f"Professor {dados.professor_id} não existe")

        materia = self.materias_dao.criar(nome=dados.nome, professor_id=dados.professor_id)

        return MateriaSchema.model_validate(materia)

    def listar_materias(self) -> List[MateriaSchema]:
        """
        Lista todas as matérias utilizando o DAO e retorna uma lista de objetos MateriaSchema.

        Returns:
            List[MateriaSchema]: Uma lista de objetos MateriaSchema representando todas as matérias.
        """
        materias = self.materias_dao.listar_todas()
        return [MateriaSchema.model_validate(m) for m in materias]

    def obter_materia_por_id(self, materia_id: int) -> MateriaSchema:
        """
        Obtém uma matéria por ID utilizando o DAO. Se a matéria não for encontrada, lança um ValueError. Caso contrário,
        retorna a matéria encontrada como um objeto MateriaSchema.

        Args:
            materia_id (int): O ID da matéria a ser obtida.

        Raises:
            ValueError: Se a matéria não for encontrada.

        Returns:
            MateriaSchema: A matéria encontrada como um objeto MateriaSchema.
        """
        materia = self.materias_dao.obter_por_id(materia_id)

        if not materia:
            raise ValueError(f"Matéria {materia_id} não encontrada")

        return MateriaSchema.model_validate(materia)

    def atualizar_materia(self, materia_id: int, dados: MateriaUpdate) -> MateriaSchema:
        """
        Verifica se a matéria existe utilizando o DAO. Se a matéria não for encontrada, lança um ValueError. Caso contrário,
        verifica se o campo "nome" está presente nos dados de atualização e se já existe uma matéria com o mesmo nome
        (excluindo a matéria atual). Se existir, lança um ValueError. Em seguida, verifica se o campo "professor_id" está
        presente e se o professor existe, caso contrário lança um ValueError. Por fim, atualiza a matéria utilizando o DAO
        e retorna a matéria atualizada como um objeto MateriaSchema.

        Args:
            materia_id (int): O ID da matéria a ser atualizada.
            dados (MateriaUpdate): Dados de atualização para a matéria.

        Raises:
            ValueError: Se a matéria não for encontrada.
            ValueError: Se já existir uma matéria com o mesmo nome.
            ValueError: Se o professor_id fornecido não existir.

        Returns:
            MateriaSchema: A matéria atualizada como um objeto MateriaSchema.
        """
        materia = self.materias_dao.obter_por_id(materia_id)
        if not materia:
            raise ValueError(f"Matéria {materia_id} não encontrada")

        dados_dict = dados.model_dump(exclude_unset=True)

        if 'nome' in dados_dict and dados_dict['nome']:
            nome_existe = self.materias_dao.obter_por_nome(dados_dict['nome'])
            if nome_existe and nome_existe.id != materia_id:
                raise ValueError(f"Matéria '{dados_dict['nome']}' já existe")

        if 'professor_id' in dados_dict and dados_dict['professor_id']:
            if not self.professor_dao.obter_por_id(dados_dict['professor_id']):
                raise ValueError(f"Professor {dados_dict['professor_id']} não existe")

        materia_atualizada = self.materias_dao.atualizar(materia_id, **dados_dict)

        return MateriaSchema.model_validate(materia_atualizada)

    def deletar_materia(self, materia_id: int) -> Dict:
        """
        Verifica se a matéria existe utilizando o DAO. Se a matéria não for encontrada, lança um ValueError. Caso contrário,
        lista todos os alunos associados à matéria utilizando o DAO e deleta cada associação. Por fim, deleta a matéria
        utilizando o DAO e retorna um dicionário contendo o ID da matéria deletada, um indicador de que a matéria foi deletada
        e a quantidade de alunos que foram removidos.

        Args:
            materia_id (int): O ID da matéria a ser deletada.

        Raises:
            ValueError: Se a matéria não for encontrada.

        Returns:
            Dict: Com os dados da matéria deletada e a quantidade de alunos removidos.
        """
        materia = self.materias_dao.obter_por_id(materia_id)
        if not materia:
            raise ValueError(f"Matéria {materia_id} não encontrada")

        alunos = self.mutantes_materias_dao.listar_por_materia(materia_id)
        for aluno in alunos:
            self.mutantes_materias_dao.deletar(aluno.id)

        self.materias_dao.deletar(materia_id)

        return {
            "id": materia_id,
            "deletado": True,
            "alunos_removidos": len(alunos)
        }

    def listar_materias_por_professor(self, professor_id: int) -> List[MateriaSchema]:
        """
        Verifica se o professor existe utilizando o DAO. Se o professor não for encontrado, lança um ValueError. Caso contrário,
        lista todas as matérias associadas ao professor utilizando o DAO e retorna uma lista de objetos MateriaSchema.

        Args:
            professor_id (int): O ID do professor cujas matérias serão listadas.

        Raises:
            ValueError: Se o professor não for encontrado.

        Returns:
            List[MateriaSchema]: Uma lista de objetos MateriaSchema representando as matérias do professor.
        """
        professor = self.professor_dao.obter_por_id(professor_id)
        if not professor:
            raise ValueError(f"Professor {professor_id} não encontrado")

        materias = self.materias_dao.listar_por_professor(professor_id)
        return [MateriaSchema.model_validate(m) for m in materias]

    def desempenho_materia(self, materia_id: int) -> Dict:
        """
        Verifica se a matéria existe utilizando o DAO. Se a matéria não for encontrada, lança um ValueError. Em seguida,
        lista todos os registros de alunos matriculados na matéria utilizando o DAO. Se não houver registros, lança um ValueError.
        Caso contrário, calcula estatísticas de desempenho incluindo: média geral, maior e menor nota, taxa de aprovação e taxa
        de reprovação. Retorna um dicionário contendo essas informações.

        Args:
            materia_id (int): O ID da matéria cujo desempenho será analisado.

        Raises:
            ValueError: Se a matéria não for encontrada.
            ValueError: Se nenhum aluno estiver matriculado na matéria.
            ValueError: Se nenhuma nota foi registrada para os alunos.

        Returns:
            Dict: Com as estatísticas de desempenho incluindo media_geral, maior_nota, menor_nota, taxa_aprovacao e taxa_reprovacao.
        """
        materia = self.materias_dao.obter_por_id(materia_id)
        if not materia:
            raise ValueError(f"Matéria {materia_id} não encontrada")

        registros = self.mutantes_materias_dao.listar_por_materia(materia_id)

        if not registros:
            raise ValueError(f"Nenhum aluno matriculado na matéria {materia_id}")

        notas = []
        aprovados = 0

        for registro in registros:
            if registro.nota1 and registro.nota2:
                media = (registro.nota1 + registro.nota2) / 2
                notas.append(media)
                if media >= 7:
                    aprovados += 1

        if not notas:
            raise ValueError("Nenhuma nota registrada")

        return {
            "materia_id": materia_id,
            "materia_nome": materia.nome,
            "total_alunos": len(registros),
            "alunos_com_notas": len(notas),
            "media_geral": round(sum(notas) / len(notas), 2),
            "maior_nota": max(notas),
            "menor_nota": min(notas),
            "taxa_aprovacao": f"{(aprovados / len(notas) * 100):.1f}%",
            "taxa_reprovacao": f"{((len(notas) - aprovados) / len(notas) * 100):.1f}%"
        }