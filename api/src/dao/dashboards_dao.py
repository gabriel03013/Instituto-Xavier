"""
Classe DAO do dashboard do professor, responsável por realizar as consultas necessárias para obter as informações relevantes 
sobre os alunos e suas notas, como total de alunos, média de notas e total de observações, além de fornecer dados para 
gráficos de barras e pizza relacionados à situação dos alunos.
"""

__author__ = ["Erik Santos", "Davi Franco"]

from sqlalchemy import select, case, func, text
from sqlalchemy.orm import Session
from models import Mutante, MutantesMaterias, Observacoes, Materias, Professor
from typing import List, Optional


class DashboardsDAO():
    def __init__(self, session: Session):
        self.session = session


    def obter_kpis_professor(self, id_professor: int):
        """
        Obtém as KPIs com Total de alunos, Média de notas e Total de observações para visualização do Professor.
        
        Args:
            id_professor (int): ID do professor para filtrar os dados
            
        Returns:
            dict: Dicionário contendo total de alunos, média de notas e total de observações
        """
        stmt = text("""
            SELECT
                (SELECT COUNT(*) FROM mutantes where esta_ativo = true) AS total_alunos,

                (
                    SELECT COALESCE(AVG((mm.nota1 + mm.nota2) / 2.0), 0.0)
                    FROM mutantesmaterias mm
                        JOIN materias mt ON mm.materia_id = mt.id
                    WHERE mt.professor_id = :id_professor
                ) AS media_notas,

                (
                    SELECT COALESCE(COUNT(ob.id), 0)
                    FROM observacoes ob
                        JOIN mutantesmaterias mm ON ob.mutantesmaterias_id = mm.id
                        JOIN materias mt ON mm.materia_id = mt.id
                    WHERE mt.professor_id = :id_professor
                ) AS total_observacoes
        """)

        result = self.session.execute(stmt, {"id_professor": id_professor}).mappings().one()

        return result
    

    def obter_notas_por_turma_materia(self, id_professor: int) -> dict:
        """ Retorna média de notas agrupada por turma e matéria para o gráfico de barras.
        
        Args:
            id_professor (int): ID do professor para filtrar os dados
            
        Returns:
            list: Lista de dicionários contendo a turma, matéria e média de notas
        """
        
        stmt = text("""
            SELECT
                t.serie || 'º Ano ' || t.turma AS turma,
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


    def obter_situacao_alunos(self, id_professor: int) -> dict:
        """
        Retorna contagem de aprovados, em recuperação e reprovados para o gráfico de pizza.
        
        Args:
            id_professor: (int) ID do professor para filtrar os dados
            
        Returns:
            dict: Dicionário contendo a contagem de alunos aprovados, em recuperação e reprovados
        """

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
    

    def obter_kpis_admin(self):
        """Obtém as KPIs com Total de Alunos, Total de Professores e Total de Turmas para visualização do Admin"""

        stmt = text(
            """
            SELECT 
                (
                    SELECT COUNT(*) FROM mutantes
                ) AS total_alunos,

                (
                    SELECT COUNT(*) FROM professores
                ) AS total_professores,

                (
                    SELECT COUNT(*) FROM turmas
                ) AS total_turmas"""
        )

        result = self.session.execute(stmt).mappings().one()
        return result
    

    def obter_graficos_admin(self):
        """ 
        Retorna média de notas agrupada por turma e matéria para o gráfico de barras.
        E quantidade de cada situação dos mutantes para gráfico de pizza.
            
        Returns:
            list: Lista de dicionários contendo a turma, matéria e média de notas, e
              quantidade de aprovações, recuperações e reprovações.
        """
            
        stmtBarras = text("""
            SELECT
                t.serie || 'º Ano ' || t.turma AS turma,
                mt.nome                             AS materia,
                AVG((mm.nota1 + mm.nota2) / 2.0)   AS media
            FROM mutantesmaterias mm
                JOIN mutantes m  ON mm.mutante_id  = m.id
                JOIN turmas t    ON m.turma_id     = t.id
                JOIN materias mt ON mm.materia_id  = mt.id
            GROUP BY t.id, mt.id
            ORDER BY t.serie, t.turma, mt.nome
        """)

        stmtPizza = text("""
            SELECT 
                CASE
                    WHEN media IS NULL THEN 'Sem Notas'
                    WHEN media >= 7 THEN 'Aprovado'
                    WHEN media >= 5 AND media < 7 THEN 'Recuperação'
                    ELSE 'Reprovado'
                END AS situacao,
                COUNT(*) AS quantidade
            FROM (
                SELECT
                    m.id AS mutante_id,
                    AVG((mm.nota1 + mm.nota2) / 2.0) AS media
                FROM mutantes m
                LEFT JOIN mutantesmaterias mm ON mm.mutante_id = m.id
                WHERE m.esta_ativo = true
                GROUP BY m.id
            ) AS medias_por_aluno
            GROUP BY situacao
        """)

        barras = self.session.execute(stmtBarras).mappings().all()
        pizza = self.session.execute(stmtPizza).mappings().all()

        return {"dashboards": {"barras": barras, "pizza": pizza}}