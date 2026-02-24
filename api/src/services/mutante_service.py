from dao.mutante_dao import MutanteDAO
from dao.poder_dao import PoderDAO
from dao.turmas_dao import TurmasDAO
from dao.mutantes_materias_dao import MutantesMateriasDAO
from schemas.mutantes_schema import MutanteBase, MutanteCreate, MutanteUpdate, MutanteResponse
from typing import List, Dict
from db.helpers.security import hash_password

class MutanteService:
    def __init__(
        self,
        mutante_dao: MutanteDAO,
        poder_dao: PoderDAO,
        turmas_dao: TurmasDAO,
        mutantes_materias_dao: MutantesMateriasDAO
    ):
        self.mutante_dao = mutante_dao
        self.poder_dao = poder_dao
        self.turmas_dao = turmas_dao
        self.mutantes_materias_dao = mutantes_materias_dao


    def registrar_novo_mutante(self, dados: MutanteCreate) -> MutanteBase:
        if self.mutante_dao.obter_matricula_vazia(dados.matricula):
            raise ValueError(f"Matrícula {dados.matricula} já existe")

        if self.mutante_dao.obter_por_email(dados.email):
            raise ValueError(f"Email {dados.email} já existe")

        # if dados.poder_id and not self.poder_dao.obter_por_id(dados.poder_id):
        #     raise ValueError(f"Poder {dados.poder_id} não existe")

        # if dados.turma_id and not self.turmas_dao.obter_por_id(dados.turma_id):
        #     raise ValueError(f"Turma {dados.turma_id} não existe")
        

        mutante = self.mutante_dao.criar(
            matricula=dados.matricula,
            nome=dados.nome,
            email=dados.email,
            senha=hash_password(dados.senha)
            # poder_id=dados.poder_id,
            # turma_id=dados.turma_id
        )

        return MutanteBase.model_validate(mutante)


    def listar_mutantes(self) -> List[MutanteBase]:
        mutantes = self.mutante_dao.listar_todos()
        return [MutanteBase.model_validate(m) for m in mutantes]


    def obter_mutante_por_id(self, mutante_id: int) -> MutanteBase:
        mutante = self.mutante_dao.obter_por_id(mutante_id)
        if not mutante:
            raise ValueError(f"Mutante {mutante_id} não encontrado")

        return MutanteBase.model_validate(mutante)


    def atualizar_mutante(self, mutante_id: int, dados: MutanteBase) -> MutanteBase:
        mutante = self.mutante_dao.obter_por_id(mutante_id)
        if not mutante:
            raise ValueError(f"Mutante {mutante_id} não encontrado")

        dados_dict = dados.dict(exclude_unset=True)

        if 'email' in dados_dict and dados_dict['email']:
            email_existe = self.mutante_dao.obter_por_email(dados_dict['email'])
            if email_existe and email_existe.id != mutante_id:
                raise ValueError(f"Email {dados_dict['email']} já existe")

        if 'poder_id' in dados_dict and dados_dict['poder_id']:
            if not self.poder_dao.obter_por_id(dados_dict['poder_id']):
                raise ValueError(f"Poder {dados_dict['poder_id']} não existe")

        if 'turma_id' in dados_dict and dados_dict['turma_id']:
            if not self.turmas_dao.obter_por_id(dados_dict['turma_id']):
                raise ValueError(f"Turma {dados_dict['turma_id']} não existe")

        mutante_atualizado = self.mutante_dao.atualizar(mutante_id, **dados_dict)

        return MutanteBase.model_validate(mutante_atualizado)
    

    def completar_cadastro(self, dados: MutanteUpdate) -> MutanteResponse:
        
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