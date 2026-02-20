from src.dao.professor_dao import ProfessorDAO
from src.dao.materias_dao import MateriasDAO
from src.schemas.professor_schema import ProfessoresSchemas
from typing import List, Dict

class ProfessorService:
    def __init__(self, professor_dao: ProfessorDAO, materias_dao: MateriasDAO):
        self.professor_dao = professor_dao
        self.materias_dao = materias_dao

    def criar_novo_professor(self, dados: ProfessoresSchemas) -> ProfessoresSchemas:
        if self.professor_dao.obter_por_usuario(dados.usuario):
            raise ValueError(f"Usuário '{dados.usuario}' já existe")

        professor = self.professor_dao.criar(
            nome=dados.nome,
            usuario=dados.usuario,
            senha=dados.senha
        )

        return ProfessoresSchemas.model_validate(professor)

    def listar_professores(self) -> List[ProfessoresSchemas]:
        professores = self.professor_dao.listar_todos()
        return [ProfessoresSchemas.model_validate(p) for p in professores]

    def obter_professor_por_id(self, professor_id: int) -> ProfessoresSchemas:
        professor = self.professor_dao.obter_por_id(professor_id)
        if not professor:
            raise ValueError(f"Professor {professor_id} não encontrado")

        return ProfessoresSchemas.model_validate(professor)

    def atualizar_professor(self, professor_id: int, dados: ProfessoresSchemas) -> ProfessoresSchemas:
        professor = self.professor_dao.obter_por_id(professor_id)
        if not professor:
            raise ValueError(f"Professor {professor_id} não encontrado")

        dados_dict = dados.dict(exclude_unset=True)

        if 'usuario' in dados_dict and dados_dict['usuario']:
            usuario_existe = self.professor_dao.obter_por_usuario(dados_dict['usuario'])
            if usuario_existe and usuario_existe.id != professor_id:
                raise ValueError(f"Usuário '{dados_dict['usuario']}' já existe")

        professor_atualizado = self.professor_dao.atualizar(professor_id, **dados_dict)

        return ProfessoresSchemas.model_validate(professor_atualizado)

    def deletar_professor(self, professor_id: int) -> Dict:
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