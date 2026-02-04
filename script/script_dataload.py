from faker import Faker
import pandas as pd
import random as rd
from helper.file_handler import write


SEED = 42
N_ROWS = 10
TABLES = {
    "Alunos": {
        "cols": ["Nome", "Email", "Senha", "Matricula", "PoderId"],    
    }
    
}

fake = Faker("pt-BR")
Faker.seed(SEED)
rd.seed(SEED)

def insert_wrapper(func):
    def wrapper(*args, **kwargs):        
        content = func(*args, **kwargs)
        write("sql/dataload.sql", content)
    return wrapper

@insert_wrapper
def generate_students(n):
    
    insert_table = f"INSERT INTO \"Alunos\" ({TABLES['Alunos']['cols_str']}) VALUES \n"
    content = ""

    try:
        for _ in range(n):
            student = {
                "Nome": fake.name(),
                "Email": fake.email(),
                "Senha": fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True),
                "Matricula": rd.randint(10000, 99999),
                "PoderId": rd.randint(1, 5),
            }
            
            content += f"('{student['Nome']}', '{student['Email']}', '{student['Senha']}', {student['Matricula']}, {student['PoderId']});\n"
        
        return insert_table, content
    
    except Exception as e:
        print(f"Erro ao gerar dados: {e}")
        