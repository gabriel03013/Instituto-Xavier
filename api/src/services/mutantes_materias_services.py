from src.dao.mutantes_materias_dao import MutantesMateriasDAO
from src.dao.mutante_dao import MutanteDAO
from src.dao.materias_dao import MateriasDAO
from src.schemas.mutantes_materias_schema import MutantesMateriasSchemas
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

    def matricular_em_materia(self, dados: MutantesMateriasSchemas) -> MutantesMateriasSchemas:
        if not self.mutante_dao.obter_por_id(dados.mutante_id):
            raise ValueError(f"Mutante {dados.mutante_id} não existe")

        if not self.materias_dao.obter_por_id(dados.materia_id):
            raise ValueError(f"Matéria {dados.materia_id} não existe")

        if self.mutantes_materias_dao.obter_por_mutante_e_materia(dados.mutante_id, dados.materia_id):
            raise ValueError(f"Mutante {dados.mutante_id} já matriculado na matéria {dados.materia_id}")

        registro = self.mutantes_materias_dao.criar(
            mutante_id=dados.mutante_id,
            materia_id=dados.materia_id,
            nota1=dados.nota_1,
            nota2=dados.nota_2
        )

        return MutantesMateriasSchemas.model_validate(registro)

    def listar_materias_mutante(self, mutante_id: int) -> List[MutantesMateriasSchemas]:
        mutante = self.mutante_dao.obter_por_id(mutante_id)
        if not mutante:
            raise ValueError(f"Mutante {mutante_id} não encontrado")

        registros = self.mutantes_materias_dao.listar_por_mutante(mutante_id)
        return [MutantesMateriasSchemas.model_validate(r) for r in registros]

    def listar_mutantes_materia(self, materia_id: int) -> List[MutantesMateriasSchemas]:
        materia = self.materias_dao.obter_por_id(materia_id)
        if not materia:
            raise ValueError(f"Matéria {materia_id} não encontrada")

        registros = self.mutantes_materias_dao.listar_por_materia(materia_id)
        return [MutantesMateriasSchemas.model_validate(r) for r in registros]

    def lancar_notas(self, mutante_id: int, materia_id: int, dados: MutantesMateriasSchemas) -> MutantesMateriasSchemas:
        if dados.nota_1 is not None and not (0 <= dados.nota_1 <= 10):
            raise ValueError("Nota 1 deve estar entre 0 e 10")

        if dados.nota_2 is not None and not (0 <= dados.nota_2 <= 10):
            raise ValueError("Nota 2 deve estar entre 0 e 10")

        registro = self.mutantes_materias_dao.obter_por_mutante_e_materia(mutante_id, materia_id)
        if not registro:
            raise ValueError(f"Mutante {mutante_id} não está matriculado na matéria {materia_id}")

        registro_atualizado = self.mutantes_materias_dao.atualizar_notas(
            registro.id,
            nota1=dados.nota_1,
            nota2=dados.nota_2
        )

        return MutantesMateriasSchemas.model_validate(registro_atualizado)

    def obter_registro_detalhes(self, mutante_id: int, materia_id: int) -> MutantesMateriasSchemas:
        registro = self.mutantes_materias_dao.obter_por_mutante_e_materia(mutante_id, materia_id)
        if not registro:
            raise ValueError("Registro não encontrado")

        return MutantesMateriasSchemas.model_validate(registro)

    def remover_matricula(self, mutante_id: int, materia_id: int) -> Dict:
        registro = self.mutantes_materias_dao.obter_por_mutante_e_materia(mutante_id, materia_id)
        if not registro:
            raise ValueError("Registro não encontrado")

        self.mutantes_materias_dao.deletar(registro.id)

        return {
            "mutante_id": mutante_id,
            "materia_id": materia_id,
            "removido": True
        }