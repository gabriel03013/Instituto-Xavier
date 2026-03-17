from database import Session
from models import Mutante
import os

session = Session()

try:
    mutantes = session.query(Mutante).all()
    print(f"Total Mutantes: {len(mutantes)}")
    for m in mutantes:
        print(f"ID: {m.id}, Nome: {m.nome}, Email: {m.email}, Matrícula: {m.matricula}")
except Exception as e:
    print(f"Erro: {e}")
finally:
    session.close()
