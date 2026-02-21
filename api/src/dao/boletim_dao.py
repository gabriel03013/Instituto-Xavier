from sqlalchemy import select, case
from sqlalchemy.orm import Session
from models import Professor, Materias, MutantesMaterias
from typing import List, Optional

class BoletimDAO:
    def __init__(self, session: Session):
        self.session = session

    def obter_minhas_notas(self, id_mutante: int) -> a:
        """Obtém o boletim do aluno"""
        media_aritmetica = (((MutantesMaterias.nota1 + MutantesMaterias.nota2) / 2))
        
        status_case = case(
            (media_aritmetica < 7, "Reprovado"),
            else_="Aprovado" 
        ).label("status")
        
        stmt = (
            select(
                Professor.nome.label("professor"), 
                Materias.nome.label("materia"), 
                MutantesMaterias.nota1, 
                MutantesMaterias.nota2, 
                media_aritmetica.label("media_final"), 
                status_case    
            )
            .join(Materias, Materias.professor_id == Professor.id)
            .join(MutantesMaterias, MutantesMaterias.materia_id == Materias.id)
            .where(MutantesMaterias.mutante_id == id_mutante)
        )

        result = self.session.execute(stmt).mappings().all() # Returns an array of dicts

        return result