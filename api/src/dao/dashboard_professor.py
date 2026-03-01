from sqlalchemy import select, case, func, text
from sqlalchemy.orm import Session
from models import Mutante, MutantesMaterias, Observacoes, Materias, Professor
from typing import List, Optional


class DashboardProfessorDAO():
    def __init__(self, session: Session):
        self.session = session

    def obter_dashboard(self, id_professor: int):
        """Obtém o dashboard com Total de alunos, Média de notas e Total de observações."""

        #TODO if we'll use the code below, we have to fix it
        
        # media_aritmetica = (MutantesMaterias.nota1 + MutantesMaterias.nota2) / 2
        
            # select(
            #     func.count(func.distinct(Mutante.id)).label("total_alunos"),
            #     func.avg(media_aritmetica).label("media_notas"), # Average from all mutants average
            #     func.count(Observacoes.id).label("total_observacoes")
            # )
            # .join(MutantesMaterias, MutantesMaterias.mutante_id == Mutante.id)
            # .join(Materias, Materias.id == MutantesMaterias.materia_id)
            # .outerjoin(Observacoes, MutantesMaterias.id == Observacoes.mutantesmaterias_id)
            # .where(Materias.professor_id == id_professor)

        # TODO: FILTER MUTANTES WHO HAVE esta_ativo = TRUE
        stmt = text("""
            SELECT
                (SELECT COUNT(*) FROM mutantes) AS total_alunos,

                (
                    SELECT AVG((mm.nota1 + mm.nota2) / 2)
                    FROM mutantesmaterias mm
                        JOIN materias mt ON mm.materia_id = mt.id
                    WHERE mt.professor_id = :id_professor
                ) AS media_notas,

                (
                    SELECT COUNT(ob.id)
                    FROM observacoes ob
                        JOIN mutantesmaterias mm ON ob.mutantesmaterias_id = mm.id
                        JOIN materias mt ON mm.materia_id = mt.id
                    WHERE mt.professor_id = :id_professor
                ) AS total_observacoes
        """)

        result = self.session.execute(stmt, {"id_professor": id_professor}).mappings().one()

        return result
    
    def obter_notas_por_turma_materia(self, id_professor: int):
        """Retorna média de notas agrupada por turma e matéria para o gráfico de barras."""

        stmt = text("""
            SELECT
                CONCAT(t.serie, 'º Ano ', t.turma) AS turma,
                mt.nome                             AS materia,
                AVG((mm.nota1 + mm.nota2) / 2.0)   AS media
            FROM mutantesmaterias mm
                JOIN mutantes m  ON mm.mutante_id  = m.id
                JOIN turmas t    ON m.turma_id     = t.id
                JOIN materias mt ON mm.materia_id  = mt.id
            WHERE mt.professor_id = :id_professor
            GROUP BY t.id, mt.id
            ORDER BY t.serie, t.turma, mt.nome
        """)

        result = self.session.execute(stmt, {"id_professor": id_professor}).mappings().all()
        return result


    def obter_situacao_alunos(self, id_professor: int):
        """Retorna contagem de aprovados, em recuperação e reprovados para o gráfico de pizza."""

        stmt = text("""
            SELECT
                COUNT(CASE WHEN media >= 7               THEN 1 END) AS aprovados,
                COUNT(CASE WHEN media >= 5 AND media < 7 THEN 1 END) AS recuperacao,
                COUNT(CASE WHEN media < 5                THEN 1 END) AS reprovados
            FROM (
                SELECT
                    mm.mutante_id,
                    AVG((mm.nota1 + mm.nota2) / 2.0) AS media
                FROM mutantesmaterias mm
                    JOIN materias mt ON mm.materia_id = mt.id
                WHERE mt.professor_id = :id_professor
                GROUP BY mm.mutante_id
            ) AS medias_por_aluno
        """)

        result = self.session.execute(stmt, {"id_professor": id_professor}).mappings().one()
        return result