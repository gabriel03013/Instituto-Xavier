from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Turma(Base):
    __tablename__ = "turmas"

    id = Column("id", Integer, primary_key=True)
    turma = Column("turma", String(15))

    def __init__(self, turma):
        self.turma = turma


class Mutante(Base):
    __tablename__ = "mutantes"

    id = Column("id", Integer, primary_key=True)
    nome = Column("nome", String(100), nullable=False)
    matricula = Column("matricula", String(50), nullable=False, unique=True)
    email = Column("email", String(100), nullable=False, unique=True)
    senha = Column("senha", String(100), nullable=False)
    poder_id = Column("poder_id", ForeignKey("poderes.id"))
    turma_id = Column("turma_id", ForeignKey("turmas.id"))

    def __init__(self, nome, matricula, email, senha, poder_id):
        self.nome = nome
        self.matricula = matricula
        self.email = email
        self.senha = senha
        self.poder_id = poder_id


class Poder(Base):
    __tablename__ = "poderes"

    id = Column("id", Integer, primary_key=True)
    nome = Column("nome", String(100), nullable=False, unique=True)

    def __init__(self, nome):
        self.nome = nome


class Professor(Base):
    __tablename__ = "professores"

    id = Column("id", Integer, primary_key=True)
    nome = Column("nome", String(100), nullable=False)
    usuario = Column("usuario", String(50), nullable=False, unique=True)
    senha = Column("senha", String(100), nullable=False)

    def __init__(self, nome, usuario, senha):
        self.nome = nome
        self.usuario = usuario,
        self.senha = senha


class Materias(Base):
    __tablename__ = "materias"

    id = Column("id", Integer, primary_key=True)
    nome = Column("nome", String(100), nullable=False, unique=True)
    professor_id = Column("professor_id", ForeignKey("professores.id"))

    def __init__(self, nome, professor_id):
        self.nome = nome,
        self.professor_id = professor_id


class MutantesMaterias(Base):
    __tablename__ = "mutantesmaterias"

    id = Column("id", Integer, primary_key=True)
    nota1 = Column("nota1", Integer, default=0)
    nota2 = Column("nota2", Integer, default=0)
    mutante_id = Column("mutante", Integer, ForeignKey("mutantes.id"))
    materia_id = Column("materia_id", Integer, ForeignKey("materias.id"))

    def __init__(self, nota1, nota2, mutante_id, materia_id):
        self.nota1 = nota1,
        self.nota2 = nota2,
        self.mutante_id = mutante_id,
        self.materia_id = materia_id


class Observacao(Base):
    __tablename__ = "observacoes"

    id = Column("id", Integer, primary_key=True)
    observacao = Column("observacao", String)

    def __init__(self, observacao):
        self.observacao = observacao