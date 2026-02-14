from sqlalchemy.orm import Session
from models import MutantesMaterias
from typing import List, Optional

class MutantesMateriasDAO:
    def __init__(self, session: Session):
        self.session = session

    def criar(self, mutante_id: int, materia_id: int, 
              nota1: Optional[int] = None, nota2: Optional[int] = None) -> MutantesMaterias:
        """Cria um registro mutante-matéria."""

        novo_registro = MutantesMaterias(
            mutante_id=mutante_id,
            materia_id=materia_id,
            nota1=nota1,
            nota2=nota2
        )
        self.session.add(novo_registro)
        self.session.commit()
        self.session.refresh(novo_registro)
        return novo_registro

    def obter_por_id(self, registro_id: int) -> Optional[MutantesMaterias]:
        """Obtém um registro pelo ID."""

        return self.session.query(MutantesMaterias).filter(MutantesMaterias.id == registro_id).first()

    def obter_por_mutante_e_materia(self, mutante_id: int, 
                                     materia_id: int) -> Optional[MutantesMaterias]:
        """Obtém registro de mutante e matéria."""

        return self.session.query(MutantesMaterias).filter(
            (MutantesMaterias.mutante_id == mutante_id) &
            (MutantesMaterias.materia_id == materia_id)
        ).first()

    def listar_por_mutante(self, mutante_id: int) -> List[MutantesMaterias]:
        """Lista matérias de um mutante."""

        return self.session.query(MutantesMaterias).filter(MutantesMaterias.mutante_id == mutante_id).all()

    def listar_por_materia(self, materia_id: int) -> List[MutantesMaterias]:
        """Lista mutantes de uma matéria."""

        return self.session.query(MutantesMaterias).filter(MutantesMaterias.materia_id == materia_id).all()

    def listar_todos(self) -> List[MutantesMaterias]:
        """Lista todos os registros."""

        return self.session.query(MutantesMaterias).all()

    def atualizar_notas(self, registro_id: int, nota1: Optional[int] = None, 
                        nota2: Optional[int] = None) -> Optional[MutantesMaterias]:
        """Atualiza as notas de um registro."""

        registro = self.session.query(MutantesMaterias).filter(MutantesMaterias.id == registro_id).first()
        if registro:
            if nota1 is not None:
                registro.nota1 = nota1
            if nota2 is not None:
                registro.nota2 = nota2
            self.session.commit()
            self.session.refresh(registro)
        return registro

    def deletar(self, registro_id: int) -> bool:
        """Deleta um registro."""

        registro = self.session.query(MutantesMaterias).filter(MutantesMaterias.id == registro_id).first()
        if registro:
            self.session.delete(registro)
            self.session.commit()
            return True
        return False