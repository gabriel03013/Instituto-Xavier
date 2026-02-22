from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, SmallInteger, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Mutante(Base):
    __tablename__ = "mutantes"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    matricula = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), unique=True)
    senha = Column(String(100))
    esta_ativo = Column(Boolean, nullable=False, default=False)
    
    poder_id = Column(Integer, ForeignKey("poderes.id"))
    poder = relationship("Poder", back_populates="mutantes")

    turma_id = Column(Integer, ForeignKey("turmas.id"))
    turma = relationship("Turmas", back_populates="mutantes")

    mutantesmaterias = relationship("MutantesMaterias", back_populates="mutante")


class Poder(Base):
    __tablename__ = "poderes"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)

    mutantes = relationship("Mutante", back_populates="poder")


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

    professor_id = Column(Integer, ForeignKey("professores.id"))
    professor = relationship("Professor", back_populates="materias")

    mutantesmaterias = relationship("MutantesMaterias", back_populates="materias")


class MutantesMaterias(Base):
    __tablename__ = "mutantesmaterias"

    id = Column(Integer, primary_key=True)
    nota1 = Column(Integer, default=0)
    nota2 = Column(Integer, default=0)

    mutante_id = Column(Integer, ForeignKey("mutantes.id"))
    mutante = relationship("Mutante", back_populates="mutantesmaterias")
    
    materia_id = Column(Integer, ForeignKey("materias.id"))
    materias = relationship("Materias", back_populates="mutantesmaterias")

    observacoes = relationship("Observacoes", back_populates="mutantesmaterias")


class Turmas(Base):
    __tablename__ = "turmas"

    id = Column(Integer, primary_key=True)
    serie = Column(SmallInteger, nullable=False)
    turma = Column(String(1), nullable=False)

    mutantes = relationship("Mutante", back_populates="turma")
    
    
class Observacoes(Base):
    __tablename__ = "observacoes"

    id = Column(Integer, primary_key=True)
    observacao = Column(Text, nullable=False)
    data = Column(Date, nullable=False)

    mutantesmaterias_id = Column(Integer, ForeignKey("mutantesmaterias.id"))
    mutantesmaterias = relationship("MutantesMaterias", back_populates="observacoes")