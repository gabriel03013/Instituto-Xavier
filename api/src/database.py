"""
Conexão com o banco de dados e inicialização da sessão para consultas e operações CRUD
"""

__author__ = ["Gabriel Mendes", "Erik Santos"]

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# Getting variables from .env
DATABASE_URL = os.getenv("DB_URI")

engine = create_engine(
    DATABASE_URL,
    echo=False
)
Session = sessionmaker(bind=engine)


Base = declarative_base() # Create base of database