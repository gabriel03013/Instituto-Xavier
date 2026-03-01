from dao.professor_dao import ProfessorDAO
from dao.materias_dao import MateriasDAO
from schemas.professores_schema import ProfessorCreate, ProfessorUpdate, ProfessorSchema
from typing import List, Dict

class ProfessorService:
    def __init__(self, professor_dao: ProfessorDAO, materias_dao: MateriasDAO):
        self.professor_dao = professor_dao
        self.materias_dao = materias_dao
        


    def criar_novo_professor(self, dados: ProfessorCreate) -> ProfessorSchema:
        if self.professor_dao.obter_por_usuario(dados.usuario):
            raise ValueError(f"Usuário '{dados.usuario}' já existe")

        professor = self.professor_dao.criar(
            nome=dados.nome,
            usuario=dados.usuario,
            senha=dados.senha
        )

        return ProfessorSchema.model_validate(professor)


    def listar_professores(self) -> List[ProfessorSchema]:
        professores = self.professor_dao.listar_todos()
        return [ProfessorSchema.model_validate(p) for p in professores]


    def obter_professor_por_id(self, professor_id: int) -> ProfessorSchema:
        professor = self.professor_dao.obter_por_id(professor_id)
        if not professor:
            raise ValueError(f"Professor {professor_id} não encontrado")

        return ProfessorSchema.model_validate(professor)


    def atualizar_professor(self, professor_id: int, dados: ProfessorUpdate) -> ProfessorSchema:
        professor = self.professor_dao.obter_por_id(professor_id)
        if not professor:
            raise ValueError(f"Professor {professor_id} não encontrado")

        dados_dict = dados.dict(exclude_unset=True)

        if 'usuario' in dados_dict and dados_dict['usuario']:
            usuario_existe = self.professor_dao.obter_por_usuario(dados_dict['usuario'])
            if usuario_existe and usuario_existe.id != professor_id:
                raise ValueError(f"Usuário '{dados_dict['usuario']}' já existe")

        professor_atualizado = self.professor_dao.atualizar(professor_id, **dados_dict)

        return ProfessorSchema.model_validate(professor_atualizado)


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