"""
Classes Models com as colunas e tipos de dados relacionados e referentes ao banco de dados.
Utilizado para a validação dos dados no dataload.
"""

__author__ = ["Davi Franco", "Erik Santos", "Gabriel Mendes"]

from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, SmallInteger, Boolean, DateTime, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, date
from database import Base


class Mutante(Base):
    __tablename__ = "mutantes"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    matricula = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), unique=True)
    senha = Column(String(100))
    esta_ativo = Column(Boolean, nullable=False, default=False)

    turma_id = Column(Integer, ForeignKey("turmas.id", ondelete="CASCADE"))
    turma = relationship("Turmas", back_populates="mutantes")

    mutantesmaterias = relationship("MutantesMaterias", back_populates="mutante", cascade="all, delete-orphan")
    tarefas = relationship("Tarefa", back_populates="mutante")

    @property
    def media1(self):
        if not self.mutantesmaterias:
            return None
        notas = [mm.nota1 for mm in self.mutantesmaterias if mm.nota1 is not None]
        return sum(notas) / len(notas) if notas else None

    @property
    def media2(self):
        if not self.mutantesmaterias:
            return None
        notas = [mm.nota2 for mm in self.mutantesmaterias if mm.nota2 is not None]
        return sum(notas) / len(notas) if notas else None

    @property
    def media_final(self):
        if self.media1 is None or self.media2 is None:
            return None
        return (self.media1 + self.media2) / 2


class Professor(Base):
    __tablename__ = "professores"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    usuario = Column(String(50), nullable=False, unique=True)
    senha = Column(String(100), nullable=False)

    materias = relationship("Materias", back_populates="professor")


class Materias(Base):
    __tablename__ = "materias"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)

    professor_id = Column(Integer, ForeignKey("professores.id", ondelete="CASCADE"))
    professor = relationship("Professor", back_populates="materias")

    mutantesmaterias = relationship("MutantesMaterias", back_populates="materias")


class MutantesMaterias(Base):
    __tablename__ = "mutantesmaterias"

    id = Column(Integer, primary_key=True)
    nota1 = Column(Integer, default=0)
    nota2 = Column(Integer, default=0)

    mutante_id = Column(Integer, ForeignKey("mutantes.id", ondelete="CASCADE"))
    mutante = relationship("Mutante", back_populates="mutantesmaterias")
    
    materia_id = Column(Integer, ForeignKey("materias.id", ondelete="CASCADE"))
    materias = relationship("Materias", back_populates="mutantesmaterias")

    quiz = Column(JSON, default=[])

    observacoes = relationship("Observacoes", back_populates="mutantesmaterias", cascade="all, delete-orphan")


class Turmas(Base):
    __tablename__ = "turmas"

    id = Column(Integer, primary_key=True)
    serie = Column(SmallInteger, nullable=False)
    turma = Column(String(1), nullable=False)

    mutantes = relationship("Mutante", back_populates="turma")

    @property
    def alunos(self):
        return self.mutantes
    
    
class Observacoes(Base):
    __tablename__ = "observacoes"

    id = Column(Integer, primary_key=True)
    observacao = Column(Text, nullable=False)
    data = Column(Date, nullable=False)

    mutantesmaterias_id = Column(Integer, ForeignKey("mutantesmaterias.id", ondelete="CASCADE"))
    mutantesmaterias = relationship("MutantesMaterias", back_populates="observacoes")

    @property
    def aluno(self):
        return self.mutantesmaterias.mutante

    @property
    def materia(self):
        return self.mutantesmaterias.materias.nome

    @property
    def professor(self):
        return self.mutantesmaterias.materias.professor.nome


class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True)
    titulo = Column(String(30), nullable=False)
    descricao = Column(Text)
    status = Column(Enum("Pendente", "Em andamento", "Cancelada", "Concluída"), default="Pendente", nullable=False)
    prioridade = Column(Enum("Baixa", "Média", "Alta"))
    data_criacao = Column(DateTime, default=datetime.utcnow)
    data_limite = Column(DateTime)
    data_conclusao = Column(DateTime)

    mutante_id = Column(Integer, ForeignKey("mutantes.id", ondelete="CASCADE"))
    mutante = relationship("Mutante", back_populates="tarefas")