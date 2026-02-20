from src.dao.poder_dao import PoderDAO
from src.schemas.poderes_schema import PoderesSchema
from typing import List, Dict

class PoderService:
    def __init__(self, poder_dao: PoderDAO):
        self.poder_dao = poder_dao

    def criar_novo_poder(self, dados: PoderesSchema) -> PoderesSchema:
        if self.poder_dao.obter_por_nome(dados.nome):
            raise ValueError(f"Poder '{dados.nome}' já existe")

        poder = self.poder_dao.criar(nome=dados.nome)

        return PoderesSchema.model_validate(poder)

    def listar_poderes(self) -> List[PoderesSchema]:
        poderes = self.poder_dao.listar_todos()
        return [PoderesSchema.model_validate(p) for p in poderes]

    def obter_poder_por_id(self, poder_id: int) -> PoderesSchema:
        poder = self.poder_dao.obter_por_id(poder_id)
        if not poder:
            raise ValueError(f"Poder {poder_id} não encontrado")

        return PoderesSchema.model_validate(poder)

    def atualizar_poder(self, poder_id: int, dados: PoderesSchema) -> PoderesSchema:
        poder = self.poder_dao.obter_por_id(poder_id)
        if not poder:
            raise ValueError(f"Poder {poder_id} não encontrado")

        dados_dict = dados.dict(exclude_unset=True)

        if 'nome' in dados_dict and dados_dict['nome']:
            nome_existe = self.poder_dao.obter_por_nome(dados_dict['nome'])
            if nome_existe and nome_existe.id != poder_id:
                raise ValueError(f"Poder '{dados_dict['nome']}' já existe")

        poder_atualizado = self.poder_dao.atualizar(poder_id, **dados_dict)

        return PoderesSchema.model_validate(poder_atualizado)

    def deletar_poder(self, poder_id: int) -> Dict:
        poder = self.poder_dao.obter_por_id(poder_id)
        if not poder:
            raise ValueError(f"Poder {poder_id} não encontrado")

        self.poder_dao.deletar(poder_id)

        return {
            "id": poder_id,
            "deletado": True
        }