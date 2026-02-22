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