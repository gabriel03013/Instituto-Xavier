from src.dao.turmas_dao import TurmasDAO
from src.dao.mutante_dao import MutanteDAO
from src.schemas.turmas_schema import TurmasSchema
from typing import List, Dict

class TurmasService:
    def __init__(self, turmas_dao: TurmasDAO, mutante_dao: MutanteDAO):
        self.turmas_dao = turmas_dao
        self.mutante_dao = mutante_dao

    def criar_nova_turma(self, dados: TurmasSchema) -> TurmasSchema:
        turma_existe = self.turmas_dao.obter_por_serie_e_turma(dados.serie, dados.turma)
        if turma_existe:
            raise ValueError(f"Turma {dados.serie}{dados.turma} já existe")

        nova_turma = self.turmas_dao.criar(serie=dados.serie, turma=dados.turma)

        return TurmasSchema.model_validate(nova_turma)

    def listar_turmas(self) -> List[TurmasSchema]:
        turmas = self.turmas_dao.listar_todas()
        return [TurmasSchema.model_validate(t) for t in turmas]

    def obter_turma_por_id(self, turma_id: int) -> TurmasSchema:
        turma = self.turmas_dao.obter_por_id(turma_id)
        if not turma:
            raise ValueError(f"Turma {turma_id} não encontrada")

        return TurmasSchema.model_validate(turma)

    def listar_turmas_por_serie(self, serie: int) -> List[TurmasSchema]:
        turmas = self.turmas_dao.listar_por_serie(serie)
        return [TurmasSchema.model_validate(t) for t in turmas]

    def atualizar_turma(self, turma_id: int, dados: TurmasSchema) -> TurmasSchema:
        turma = self.turmas_dao.obter_por_id(turma_id)
        if not turma:
            raise ValueError(f"Turma {turma_id} não encontrada")

        dados_dict = dados.dict(exclude_unset=True)

        if 'serie' in dados_dict and 'turma' in dados_dict:
            turma_existe = self.turmas_dao.obter_por_serie_e_turma(
                dados_dict['serie'],
                dados_dict['turma']
            )
            if turma_existe and turma_existe.id != turma_id:
                raise ValueError(f"Turma {dados_dict['serie']}{dados_dict['turma']} já existe")

        turma_atualizada = self.turmas_dao.atualizar(turma_id, **dados_dict)

        return TurmasSchema.model_validate(turma_atualizada)

    def deletar_turma(self, turma_id: int) -> Dict:
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