from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, SmallInteger
from db.connection.database import Base


class Mutant(Base):
    __tablename__ = "mutantes"

    id = Column(Integer, primary_key=True)
    matricula = Column(String(50), nullable=False, unique=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha = Column(String(100), nullable=False)
    poder_id = Column(Integer, ForeignKey("poderes.id"))
    turma_id = Column(Integer, ForeignKey("turmas.id"))

class Poder(Base):
    __tablename__ = "poderes"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)


class Professor(Base):
    __tablename__ = "professores"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    usuario = Column(String(50), nullable=False, unique=True)
    senha = Column(String(100), nullable=False)


class Materias(Base):
    __tablename__ = "materias"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    professor_id = Column(Integer, ForeignKey("professores.id"))

class MutantesMaterias(Base):
    __tablename__ = "mutantesmaterias"

    id = Column(Integer, primary_key=True)
    mutante_id = Column(Integer, ForeignKey("mutantes.id"))
    materia_id = Column(Integer, ForeignKey("materias.id"))
    nota1 = Column(Integer)
    nota2 = Column(Integer)
class Turmas(Base):
    __tablename__ = "turmas"

    id = Column(Integer, primary_key=True)
    serie = Column(SmallInteger, nullable=False)
    turma = Column(String(1), nullable=False)
    
class Observacoes(Base):
    __tablename__ = "observacoes"

    id = Column(Integer, primary_key=True)
    mutantesmaterias_id = Column(Integer, ForeignKey("mutantesmaterias.id"))
    observacao = Column(Text, nullable=False)
    data = Column(Date, nullable=False)