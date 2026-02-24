from src.dao.observacoes_dao import ObservacoesDAO
from src.dao.mutantes_materias_dao import MutantesMateriasDAO
from src.schemas.observacoes_schema import ObservacoesSchemas
from typing import List, Dict
from datetime import date

class ObservacoesService:
    def __init__(self, observacoes_dao: ObservacoesDAO, mutantes_materias_dao: MutantesMateriasDAO):
        self.observacoes_dao = observacoes_dao
        self.mutantes_materias_dao = mutantes_materias_dao

    def adicionar_observacao(self, dados: ObservacoesSchemas) -> ObservacoesSchemas:
        if not self.mutantes_materias_dao.obter_por_id(dados.mutantesmaterias_id):
            raise ValueError(f"Registro mutante-matéria {dados.mutantesmaterias_id} não encontrado")

        if not dados.observacao or len(dados.observacao.strip()) == 0:
            raise ValueError("Observação não pode estar vazia")

        obs = self.observacoes_dao.criar(
            mutantesmaterias_id=dados.mutantesmaterias_id,
            observacao=dados.observacao,
            data=dados.data
        )

        return ObservacoesSchemas.model_validate(obs)

    def listar_observacoes_registro(self, mutantesmaterias_id: int) -> List[ObservacoesSchemas]:
        if not self.mutantes_materias_dao.obter_por_id(mutantesmaterias_id):
            raise ValueError(f"Registro mutante-matéria {mutantesmaterias_id} não encontrado")

        observacoes = self.observacoes_dao.listar_por_mutante_materia(mutantesmaterias_id)
        return [ObservacoesSchemas.model_validate(o) for o in observacoes]

    def listar_observacoes_periodo(self, data_inicio: date, data_fim: date) -> List[ObservacoesSchemas]:
        observacoes = self.observacoes_dao.listar_por_data(data_inicio, data_fim)
        return [ObservacoesSchemas.model_validate(o) for o in observacoes]

    def listar_todas_observacoes(self) -> List[ObservacoesSchemas]:
        observacoes = self.observacoes_dao.listar_todas()
        return [ObservacoesSchemas.model_validate(o) for o in observacoes]

    def obter_observacao_por_id(self, observacao_id: int) -> ObservacoesSchemas:
        obs = self.observacoes_dao.obter_por_id(observacao_id)
        if not obs:
            raise ValueError(f"Observação {observacao_id} não encontrada")

        return ObservacoesSchemas.model_validate(obs)

    def atualizar_observacao(self, observacao_id: int, dados: ObservacoesSchemas) -> ObservacoesSchemas:
        obs = self.observacoes_dao.obter_por_id(observacao_id)
        if not obs:
            raise ValueError(f"Observação {observacao_id} não encontrada")

        dados_dict = dados.dict(exclude_unset=True)

        if 'observacao' in dados_dict and dados_dict['observacao']:
            if not dados_dict['observacao'].strip():
                raise ValueError("Observação não pode estar vazia")

        obs_atualizada = self.observacoes_dao.atualizar(observacao_id, **dados_dict)

        return ObservacoesSchemas.model_validate(obs_atualizada)

    def deletar_observacao(self, observacao_id: int) -> Dict:
        obs = self.observacoes_dao.obter_por_id(observacao_id)
        if not obs:
            raise ValueError(f"Observação {observacao_id} não encontrada")

        self.observacoes_dao.deletar(observacao_id)

        return {
            "id": observacao_id,
            "deletado": True
        }