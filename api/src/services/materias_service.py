from src.dao.materias_dao import MateriasDAO
from src.dao.professor_dao import ProfessorDAO
from src.dao.mutantes_materias_dao import MutantesMateriasDAO
from src.schemas.materia_schema import MateriasSchema
from typing import List, Dict

class MateriasService:
    def __init__(
        self,
        materias_dao: MateriasDAO,
        professor_dao: ProfessorDAO,
        mutantes_materias_dao: MutantesMateriasDAO
    ):
        self.materias_dao = materias_dao
        self.professor_dao = professor_dao
        self.mutantes_materias_dao = mutantes_materias_dao

    def criar_nova_materia(self, dados: MateriasSchema) -> MateriasSchema:
        if self.materias_dao.obter_por_nome(dados.nome):
            raise ValueError(f"Matéria '{dados.nome}' já existe")

        if not self.professor_dao.obter_por_id(dados.professor_id):
            raise ValueError(f"Professor {dados.professor_id} não existe")

        materia = self.materias_dao.criar(nome=dados.nome, professor_id=dados.professor_id)

        return MateriasSchema.model_validate(materia)

    def listar_materias(self) -> List[MateriasSchema]:
        materias = self.materias_dao.listar_todas()
        return [MateriasSchema.model_validate(m) for m in materias]

    def obter_materia_por_id(self, materia_id: int) -> MateriasSchema:
        materia = self.materias_dao.obter_por_id(materia_id)

        if not materia:
            raise ValueError(f"Matéria {materia_id} não encontrada")

        return MateriasSchema.model_validate(materia)

    def atualizar_materia(self, materia_id: int, dados: MateriasSchema) -> MateriasSchema:
        materia = self.materias_dao.obter_por_id(materia_id)
        if not materia:
            raise ValueError(f"Matéria {materia_id} não encontrada")

        dados_dict = dados.dict(exclude_unset=True)

        if 'nome' in dados_dict and dados_dict['nome']:
            nome_existe = self.materias_dao.obter_por_nome(dados_dict['nome'])
            if nome_existe and nome_existe.id != materia_id:
                raise ValueError(f"Matéria '{dados_dict['nome']}' já existe")

        if 'professor_id' in dados_dict and dados_dict['professor_id']:
            if not self.professor_dao.obter_por_id(dados_dict['professor_id']):
                raise ValueError(f"Professor {dados_dict['professor_id']} não existe")

        materia_atualizada = self.materias_dao.atualizar(materia_id, **dados_dict)

        return MateriasSchema.model_validate(materia_atualizada)

    def deletar_materia(self, materia_id: int) -> Dict:
        materia = self.materias_dao.obter_por_id(materia_id)
        if not materia:
            raise ValueError(f"Matéria {materia_id} não encontrada")

        alunos = self.mutantes_materias_dao.listar_por_materia(materia_id)
        for aluno in alunos:
            self.mutantes_materias_dao.deletar(aluno.id)

        self.materias_dao.deletar(materia_id)

        return {
            "id": materia_id,
            "deletado": True,
            "alunos_removidos": len(alunos)
        }

    def listar_materias_por_professor(self, professor_id: int) -> List[MateriasSchema]:
        professor = self.professor_dao.obter_por_id(professor_id)
        if not professor:
            raise ValueError(f"Professor {professor_id} não encontrado")

        materias = self.materias_dao.listar_por_professor(professor_id)
        return [MateriasSchema.model_validate(m) for m in materias]

    def desempenho_materia(self, materia_id: int) -> Dict:
        materia = self.materias_dao.obter_por_id(materia_id)
        if not materia:
            raise ValueError(f"Matéria {materia_id} não encontrada")

        registros = self.mutantes_materias_dao.listar_por_materia(materia_id)

        if not registros:
            raise ValueError(f"Nenhum aluno matriculado na matéria {materia_id}")

        notas = []
        aprovados = 0

        for registro in registros:
            if registro.nota1 and registro.nota2:
                media = (registro.nota1 + registro.nota2) / 2
                notas.append(media)
                if media >= 7:
                    aprovados += 1

        if not notas:
            raise ValueError("Nenhuma nota registrada")

        return {
            "materia_id": materia_id,
            "materia_nome": materia.nome,
            "total_alunos": len(registros),
            "alunos_com_notas": len(notas),
            "media_geral": round(sum(notas) / len(notas), 2),
            "maior_nota": max(notas),
            "menor_nota": min(notas),
            "taxa_aprovacao": f"{(aprovados / len(notas) * 100):.1f}%",
            "taxa_reprovacao": f"{((len(notas) - aprovados) / len(notas) * 100):.1f}%"
        }