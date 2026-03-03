"""
Service para gerenciar as matrículas de mutantes em matérias. Este service é responsável por matricular mutantes em matérias, 
listar as matérias de um mutante, listar os mutantes de uma matéria, lançar notas para um mutante em uma matéria, obter 
detalhes de uma matrícula específica e remover uma matrícula. Ele utiliza os DAOs de mutantes, matérias e mutantes_materias 
para realizar as operações necessárias no banco de dados e retorna os resultados como objetos de esquema apropriados.
"""

__author__ = "Davi Franco"

from dao.mutantes_materias_dao import MutantesMateriasDAO
from dao.mutante_dao import MutanteDAO
from dao.materias_dao import MateriasDAO
from schemas.mutantes_materias_schema import MutantesMateriasCreate, MutantesMateriasUpdate, MutantesMateriasSchema, MutanteGradeSchema
from typing import List, Dict

class MutantesMateriasService:
    def __init__(
        self,
        mutantes_materias_dao: MutantesMateriasDAO,
        mutante_dao: MutanteDAO,
        materias_dao: MateriasDAO
    ):
        self.mutantes_materias_dao = mutantes_materias_dao
        self.mutante_dao = mutante_dao
        self.materias_dao = materias_dao

    def matricular_em_materia(self, dados: MutantesMateriasCreate) -> MutantesMateriasSchema:
        """
            Matricula um mutante em uma matéria. Verifica se o mutante e a matéria existem, e se o mutante já está 
            matriculado na matéria. Se alguma dessas condições não for atendida, lança um ValueError. Caso contrário,
            cria a matrícula utilizando o DAO e retorna a matrícula criada como um objeto MutantesMateriasSchema.

        Args:
            dados (MutantesMateriasCreate): Dados necessários para matricular um mutante em uma matéria, incluindo IDs do 
                                            mutante e da matéria, e notas iniciais.

        Raises:
            ValueError: Se o mutante não existir.
            ValueError: Se a matéria não existir.
            ValueError: Se o mutante já estiver matriculado na matéria.

        Returns:
            MutantesMateriasSchema: O objeto MutantesMateriasSchema representando a matrícula criada.
        """
        
        
        if not self.mutante_dao.obter_por_id(dados.mutante_id):
            raise ValueError(f"Mutante {dados.mutante_id} não existe")

        if not self.materias_dao.obter_por_id(dados.materia_id):
            raise ValueError(f"Matéria {dados.materia_id} não existe")

        if self.mutantes_materias_dao.obter_por_mutante_e_materia(dados.mutante_id, dados.materia_id):
            raise ValueError(f"Mutante {dados.mutante_id} já matriculado na matéria {dados.materia_id}")

        registro = self.mutantes_materias_dao.criar(
            mutante_id=dados.mutante_id,
            materia_id=dados.materia_id,
            nota1=dados.nota1,
            nota2=dados.nota2
        )

        return MutantesMateriasSchema.model_validate(registro)

    def listar_materias_mutante(self, mutante_id: int) -> List[MutantesMateriasSchema]:
        """
            Lista as matérias em que um mutante está matriculado, incluindo as notas. Verifica se o mutante existe, e se não 
            existir, lança um ValueError. Caso contrário, utiliza o DAO para listar as matérias do mutante e retorna as 
            relações matéria-mutante como uma lista de objetos MutantesMateriasSchema.

        Args:
            mutante_id (int): 

        Raises:
            ValueError: caso o mutante não seja encontrado.

        Returns:
            List[MutantesMateriasSchema]:  Lista de objetos MutantesMateriasSchema representando as matérias em que o mutante 
                                            está matriculado, incluindo as notas.
        """
        
        
        mutante = self.mutante_dao.obter_por_id(mutante_id)
        if not mutante:
            raise ValueError(f"Mutante {mutante_id} não encontrado")

        registros = self.mutantes_materias_dao.listar_por_mutante(mutante_id)
        return [MutantesMateriasSchema.model_validate(r) for r in registros]
    

    def listar_mutantes_materia(self, materia_id: int) -> List[MutantesMateriasSchema]:
        """
            Lista os mutantes matriculados em uma matéria, incluindo as notas. Verifica se a matéria existe, e se não existir,
            lança um ValueError. Caso contrário, utiliza o DAO para listar os mutantes da matéria e retorna as relações
            mutante-matéria como uma lista de objetos MutantesMateriasSchema.

        Args:
            materia_id (int): ID da matéria para a qual se deseja listar os mutantes matriculados.

        Raises:
            ValueError: caso a matéria não seja encontrada.


        Returns:
            List[MutantesMateriasSchema]: Lista de objetos MutantesMateriasSchema representando os mutantes matriculados na matéria.
        """
        
        
        materia = self.materias_dao.obter_por_id(materia_id)
        if not materia:
            raise ValueError(f"Matéria {materia_id} não encontrada")

        registros = self.mutantes_materias_dao.listar_por_materia(materia_id)
        return [MutantesMateriasSchema.model_validate(r) for r in registros]
    

    def lancar_notas(self, mutante_id: int, materia_id: int, dados: MutantesMateriasUpdate) -> MutantesMateriasSchema:
        """
            Lança ou atualiza as notas de um mutante em uma matéria. Verifica se as notas estão dentro do intervalo permitido (0 a 10),
            e se o mutante está matriculado na matéria. Se alguma dessas condições não for atendida, lança um ValueError. 
            Caso contrário, utiliza o DAO para atualizar as notas do registro mutante-matéria e retorna o registro atualizado

        Args:
            mutante_id (int): ID do mutante que está sendo matriculado.
            materia_id (int): ID da matéria em que o mutante está matriculado.
            dados (MutantesMateriasUpdate): Dados com as notas a serem lançadas.

        Raises:
            ValueError: caso as notas estejam fora do intervalo permitido (0 a 10).
            ValueError: caso o mutante não esteja matriculado na matéria.
            ValueError: caso as notas estejam fora do intervalo permitido (0 a 10).

        Returns:
            MutantesMateriasSchema: Registro atualizado de mutante-matéria.
        """
        
        
        if dados.nota1 is not None and not (0 <= dados.nota1 <= 10):
            raise ValueError("Nota 1 deve estar entre 0 e 10")

        if dados.nota2 is not None and not (0 <= dados.nota2 <= 10):
            raise ValueError("Nota 2 deve estar entre 0 e 10")

        registro = self.mutantes_materias_dao.obter_por_mutante_e_materia(mutante_id, materia_id)
        if not registro:
            raise ValueError(f"Mutante {mutante_id} não está matriculado na matéria {materia_id}")

        registro_atualizado = self.mutantes_materias_dao.atualizar_notas(
            registro.id,
            nota1=dados.nota1,
            nota2=dados.nota2
        )

        return MutantesMateriasSchema.model_validate(registro_atualizado)
    

    def obter_registro_detalhes(self, mutante_id: int, materia_id: int) -> MutantesMateriasSchema:
        """Obtém os detalhes de um registro de mutante em uma matéria.

        Args:
            mutante_id (int): ID do mutante.
            materia_id (int): ID da matéria.


        Raises:
            ValueError: caso o registro não seja encontrado.

        Returns:
            MutantesMateriasSchema: Registro de mutante-matéria com detalhes.
        """
        
        
        registro = self.mutantes_materias_dao.obter_por_mutante_e_materia(mutante_id, materia_id)
        if not registro:
            raise ValueError("Registro não encontrado")

        return MutantesMateriasSchema.model_validate(registro)

    def remover_matricula(self, mutante_id: int, materia_id: int) -> Dict:
        """
            Remove a matrícula de um mutante em uma matéria. Verifica se o registro de mutante-matéria existe, e se não existir,
            lança um ValueError. Caso contrário, utiliza o DAO para deletar o registro de matrícula e retorna um dicionário 
            indicando que a matrícula foi removida.

        Args:
            mutante_id (int): ID do mutante que está sendo desmatriculado.
            materia_id (int): ID da matéria em que o mutante está matriculado.

        Raises:
            ValueError: 

        Returns:
            Dict: Dicionário indicando que a matrícula foi removida, contendo os IDs do mutante e da matéria, e um indicador de remoção.
        """

        registro = self.mutantes_materias_dao.obter_por_mutante_e_materia(mutante_id, materia_id)
        if not registro:
            raise ValueError("Registro não encontrado")

        self.mutantes_materias_dao.deletar(registro.id)

        return {
            "mutante_id": mutante_id,
            "materia_id": materia_id,
            "removido": True
        }

    def listar_grades_por_turma(self, turma_id: int, materia_id: int) -> List[MutanteGradeSchema]:
        """
        Lista as notas dos mutantes de uma turma em uma determinada matéria.
        Calcula a média final de cada mutante.
        """
        registros = self.mutantes_materias_dao.listar_por_turma_e_materia(turma_id, materia_id)
        
        grades = []
        for r in registros:
            # Nota 1 e 2 são Integer no banco, mas tratamos como float para média se necessário.
            # No esquema estão como float.
            media = (r.nota1 + r.nota2) / 2.0
            
            grade = MutanteGradeSchema(
                id=r.id,
                mutante_id=r.mutante.id,
                nome=r.mutante.nome,
                matricula=r.mutante.matricula,
                nota1=float(r.nota1),
                nota2=float(r.nota2),
                media=media
            )
            grades.append(grade)
            
        return grades