import sys
import os
from sqlalchemy import text

# Adiciona o diretório src ao path para importar a database
sys.path.append(os.path.join(os.getcwd(), 'src'))
from database import engine

def add_quiz_column():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE mutantesmaterias ADD COLUMN quiz TEXT DEFAULT '[]'"))
            conn.commit()
            print("Coluna 'quiz' adicionada com sucesso à tabela mutantesmaterias.")
        except Exception as e:
            if "already exists" in str(e).lower():
                print("A coluna 'quiz' já existe.")
            else:
                print(f"Erro ao adicionar coluna: {e}")

if __name__ == "__main__":
    add_quiz_column()
