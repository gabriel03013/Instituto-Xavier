from sqlalchemy.orm import Session
from models import Observacoes
from typing import List, Optional
from datetime import date

class ObservacoesDAO:
    def __init__(self, session: Session):
        self.session = session

    def criar(self, mutantesmaterias_id: int, observacao: str, 
              data: date) -> Observacoes:
        """Cria uma nova observação."""

        nova_observacao = Observacoes(
            mutantesmaterias_id=mutantesmaterias_id,
            observacao=observacao,
            data=data
        )
        self.session.add(nova_observacao)
        self.session.commit()
        self.session.refresh(nova_observacao)
        return nova_observacao

    def obter_por_id(self, observacao_id: int) -> Optional[Observacoes]:
        """Obtém uma observação pelo ID."""

        return self.session.query(Observacoes).filter(Observacoes.id == observacao_id).first()

    def listar_por_mutante_materia(self, mutantesmaterias_id: int) -> List[Observacoes]:
        """Lista observações de um registro."""

        return self.session.query(Observacoes).filter(
            Observacoes.mutantesmaterias_id == mutantesmaterias_id
        ).order_by(Observacoes.data.desc()).all()

    def listar_por_data(self, data_inicio: date, data_fim: date) -> List[Observacoes]:
        """Lista observações em um intervalo."""

        return self.session.query(Observacoes).filter(
            (Observacoes.data >= data_inicio) & (Observacoes.data <= data_fim)
        ).order_by(Observacoes.data.desc()).all()

    def listar_todas(self) -> List[Observacoes]:
        """Lista todas as observações."""

        return self.session.query(Observacoes).order_by(Observacoes.data.desc()).all()

    def atualizar(self, observacao_id: int, observacao: Optional[str] = None, 
                  data: Optional[date] = None) -> Optional[Observacoes]:
        """Atualiza uma observação."""

        obs = self.session.query(Observacoes).filter(Observacoes.id == observacao_id).first()
        if obs:
            if observacao is not None:
                obs.observacao = observacao
            if data is not None:
                obs.data = data
            self.session.commit()
            self.session.refresh(obs)
        return obs

    def deletar(self, observacao_id: int) -> bool:
        """Deleta uma observação."""

        observacao = self.session.query(Observacoes).filter(Observacoes.id == observacao_id).first()
        if observacao:
            self.session.delete(observacao)
            self.session.commit()
            return True
        return False