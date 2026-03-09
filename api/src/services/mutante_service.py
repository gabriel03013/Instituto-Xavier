"""
Service para gerenciar os mutantes do Instituto. Este service é responsável por criar, listar, obter, atualizar e
deletar mutantes, além de lidar com o registro inicial, conclusão de cadastro e a associação entre mutantes, poderes,
turmas e matérias. Ele utiliza os DAOs de mutantes, poderes, turmas e matérias para realizar as operações necessárias
no banco de dados e retorna os resultados como objetos de esquema apropriados.
"""

__author__ = "Davi Franco"

from dao.mutante_dao import MutanteDAO
from dao.turmas_dao import TurmasDAO
from dao.mutantes_materias_dao import MutantesMateriasDAO
from schemas.mutantes_schema import MutanteCreate, MutanteUpdate, MutanteResponse, MutanteSchema
from typing import List, Dict
from db.helpers.security import hash_password

class MutanteService:
    def __init__(
        self,
        mutante_dao: MutanteDAO,
        turmas_dao: TurmasDAO,
        mutantes_materias_dao: MutantesMateriasDAO
    ):
        self.mutante_dao = mutante_dao
        self.turmas_dao = turmas_dao
        self.mutantes_materias_dao = mutantes_materias_dao

    def registrar_novo_mutante(self, dados: MutanteCreate) -> MutanteResponse:
        mutante_existente = self.mutante_dao.obter_por_matricula(dados.matricula)
        
        if mutante_existente:
             # Se existe e está "vazia", vamos apenas completar. 
             # Se já tem nome/email, então realmente "já existe".
             if mutante_existente.nome:
                 raise ValueError(f"Matrícula {dados.matricula} já está vinculada a um aluno.")
             
             mutante = self.mutante_dao.atualizar(
                 mutante_existente.id,
                 nome=dados.nome,
                 email=dados.email,
                 senha=hash_password(dados.senha),
                 turma_id=dados.turma_id,
                 esta_ativo=True
             )
        else:
            mutante = self.mutante_dao.criar(
                matricula=dados.matricula,
                nome=dados.nome,
                email=dados.email,
                senha=hash_password(dados.senha),
                esta_ativo=True,
                turma_id=dados.turma_id
            )

        return MutanteResponse.model_validate(mutante)


    def listar_mutantes(self) -> List[MutanteSchema]:
        """
        Lista todos os mutantes utilizando o DAO e retorna uma lista de objetos MutanteSchema.

        Returns:
            List[MutanteSchema]: Uma lista de objetos MutanteSchema representando todos os mutantes.
        """
        mutantes = self.mutante_dao.listar_todos()
        return [MutanteSchema.model_validate(m) for m in mutantes]

    def obter_mutante_por_id(self, mutante_id: int) -> MutanteSchema:
        """
        Obtém um mutante por ID utilizando o DAO. Se o mutante não for encontrado, lança um ValueError. Caso contrário,
        retorna o mutante encontrado como um objeto MutanteSchema.

        Args:
            mutante_id (int): O ID do mutante a ser obtido.

        Raises:
            ValueError: Se o mutante não for encontrado.

        Returns:
            MutanteSchema: O mutante encontrado como um objeto MutanteSchema.
        """
        mutante = self.mutante_dao.obter_por_id(mutante_id)
        if not mutante:
            raise ValueError(f"Mutante {mutante_id} não encontrado")

        return MutanteSchema.model_validate(mutante)

    def atualizar_mutante(self, mutante_id: int, dados: MutanteUpdate) -> MutanteSchema:
        """
        Verifica se o mutante existe utilizando o DAO. Se o mutante não for encontrado, lança um ValueError. Caso contrário,
        verifica se o campo "email" está presente nos dados de atualização e se já existe um mutante com o mesmo email
        (excluindo o mutante atual). Se existir, lança um ValueError. Em seguida, verifica se o campo "poder_id" está presente
        e se o poder existe, caso contrário lança um ValueError. Também verifica se o campo "turma_id" está presente e se a turma
        existe, caso contrário lança um ValueError. Por fim, atualiza o mutante utilizando o DAO e retorna o mutante atualizado
        como um objeto MutanteSchema.

        Args:
            mutante_id (int): O ID do mutante a ser atualizado.
            dados (MutanteUpdate): Dados de atualização para o mutante.

        Raises:
            ValueError: Se o mutante não for encontrado.
            ValueError: Se já existir um mutante com o mesmo email.
            ValueError: Se o poder_id fornecido não existir.
            ValueError: Se o turma_id fornecido não existir.

        Returns:
            MutanteSchema: O mutante atualizado como um objeto MutanteSchema.
        """
        mutante = self.mutante_dao.obter_por_id(mutante_id)
        if not mutante:
            raise ValueError(f"Mutante {mutante_id} não encontrado")

        dados_dict = dados.model_dump(exclude_unset=True)

        if 'email' in dados_dict and dados_dict['email']:
            email_existe = self.mutante_dao.obter_por_email(dados_dict['email'])
            if email_existe and email_existe.id != mutante_id:
                raise ValueError(f"Email {dados_dict['email']} já existe")


        if 'turma_id' in dados_dict and dados_dict['turma_id']:
            if not self.turmas_dao.obter_por_id(dados_dict['turma_id']):
                raise ValueError(f"Turma {dados_dict['turma_id']} não existe")

        mutante_atualizado = self.mutante_dao.atualizar(mutante_id, **dados_dict)

        return MutanteSchema.model_validate(mutante_atualizado)

    def completar_cadastro(self, dados: MutanteUpdate) -> MutanteResponse:
        """
        Procura um mutante com matrícula vazia (cadastro incompleto) utilizando o DAO. Se o mutante não for encontrado,
        lança um ValueError. Em seguida, verifica se já existe um mutante com o email fornecido, caso exista lança um ValueError.
        Caso contrário, atualiza o mutante com os dados fornecidos (nome, email, senha criptografada e ativo) utilizando o DAO
        e retorna o mutante atualizado como um objeto MutanteResponse.

        Args:
            dados (MutanteUpdate): Dados necessários para completar o cadastro do mutante.

        Raises:
            ValueError: Se a matrícula não for encontrada ou já estiver completa.
            ValueError: Se o email já estiver em uso.

        Returns:
            MutanteResponse: O mutante com cadastro atualizado como um objeto MutanteResponse.
        """
        mutante = self.mutante_dao.obter_matricula_vazia(dados.matricula)

        if not mutante:
            raise ValueError(f"Matrícula não encontrada ou já completa.")

        if self.mutante_dao.obter_por_email(dados.email):
            raise ValueError("E-mail já está em uso.")

        mutante_atualizado = self.mutante_dao.atualizar(
            mutante.id,
            nome=dados.nome,
            email=dados.email,
            senha=hash_password(dados.senha),
            esta_ativo=True
        )

        return MutanteResponse.model_validate(mutante_atualizado)

    def deletar_mutante(self, mutante_id: int) -> Dict:
        """
        Verifica se o mutante existe utilizando o DAO. Se o mutante não for encontrado, lança um ValueError. Caso contrário,
        lista todas as matérias associadas ao mutante utilizando o DAO e deleta cada uma delas. Por fim, deleta o mutante
        utilizando o DAO e retorna um dicionário contendo o ID do mutante deletado, um indicador de que o mutante foi deletado
        e a quantidade de matérias que foram removidas.

        Args:
            mutante_id (int): O ID do mutante a ser deletado.

        Raises:
            ValueError: Se o mutante não for encontrado.

        Returns:
            Dict: Com os dados do mutante deletado e a quantidade de matérias removidas.
        """
        mutante = self.mutante_dao.obter_por_id(mutante_id)
        if not mutante:
            raise ValueError(f"Mutante {mutante_id} não encontrado")

        materias = self.mutantes_materias_dao.listar_por_mutante(mutante_id)
        for materia in materias:
            self.mutantes_materias_dao.deletar(materia.id)

        self.mutante_dao.deletar(mutante_id)

        return {
            "id": mutante_id,
            "deletado": True,
            "materias_removidas": len(materias)
        }