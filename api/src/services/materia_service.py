from typing import List, Optional, Dict
from dao.materias_dao import MateriasDAO
from schemas.materias_schema import MateriaCreate, MateriaUpdate, MateriaSchema

class MateriaService:
    def __init__(self, materias_dao: MateriasDAO):
        self.materias_dao = materias_dao

    def listar_materias(self) -> List[MateriaSchema]:
        materias = self.materias_dao.listar_todas()
        return [MateriaSchema.model_validate(m) for m in materias]

    def obter_materia_por_id(self, materia_id: int) -> MateriaSchema:
        materia = self.materias_dao.obter_por_id(materia_id)
        if not materia:
            raise ValueError(f"Materia {materia_id} não encontrada")
        return MateriaSchema.model_validate(materia)

    def criar_novo_materia(self, dados: MateriaCreate) -> MateriaSchema:
        materia = self.materias_dao.criar(nome=dados.nome, professor_id=dados.professor_id)
        return MateriaSchema.model_validate(materia)

    def atualizar_materia(self, materia_id: int, dados: MateriaUpdate) -> MateriaSchema:
        materia = self.materias_dao.obter_por_id(materia_id)
        if not materia:
            raise ValueError(f"Materia {materia_id} não encontrada")
        
        dados_dict = dados.model_dump(exclude_unset=True)
        materia_atualizada = self.materias_dao.atualizar(materia_id, **dados_dict)
        return MateriaSchema.model_validate(materia_atualizada)

    def deletar_materia(self, materia_id: int) -> Dict:
        if not self.materias_dao.deletar(materia_id):
            raise ValueError(f"Materia {materia_id} não encontrada")
        return {"id": materia_id, "deletado": True}
