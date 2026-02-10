from asyncio import tasks
import os
import random
from faker import Faker

from db.helpers.logger import logger
from db.helpers.security import hash_password

from db.database import Session, engine, Base
from db.models import Poder, Professor, Mutant, Materias, MutantesMaterias


fake = Faker('pt_BR') 
session = Session()

N_ROWS = 20
SENHA_PROFESSORES = os.getenv("SENHA_PROFESSORES")



# Poderes

def seed_poderes(n: int=10):
    poderes = []
    for _ in range(n):
        poder = Poder(nome=fake.unique.word().capitalize())
        poderes.append(poder)
    
    session.add_all(poderes)
    session.commit()
    logger.info("Poderes criados!")


# Mutantes

def seed_mutantes(n: int = 0):
    ids_poderes = [id[0] for id in session.query(Poder.id).all()]
    
    if not ids_poderes:
        logger.error("Erro: Não há poderes cadastrados. Rode create_poderes primeiro.")
        return

    mutantes = []

    for _ in range(n):
    
        mutante = Mutant(
            matricula=str(fake.unique.random_number(digits=5)),
            nome=fake.name(),
            email=fake.unique.email(),
            senha=hash_password(fake.password()), 
            poder_id=random.choice(ids_poderes) 
        )
        mutantes.append(mutante)

    session.add_all(mutantes)
    session.commit()
    logger.info("Mutantes criados!")


# Professores
def seed_professores(n: int = 0):
    professores_fixos = [
        ("Ana Souza", "ana.mat", SENHA_PROFESSORES),
        ("Carlos Lima", "carlos.port", SENHA_PROFESSORES),
        ("Juliana Rocha", "juliana.hist", SENHA_PROFESSORES),
        ("Marcos Pereira", "marcos.cien", SENHA_PROFESSORES),
        ("Diogo Nascimento", "diogo.info", SENHA_PROFESSORES),
    ]

    professores = []

    for nome, usuario, senha in professores_fixos:
        professores.append(
            Professor(
                nome=nome,
                usuario=usuario,
                senha=hash_password(senha)
            )
        )

    session.add_all(professores)
    session.commit()
    logger.info("Professores fixos inseridos com sucesso.")



# Materias
def seed_materias(n: int = 0):
    materias_fixas = [
        ("Matemática", "ana.mat"),
        ("Português", "carlos.port"),
        ("História", "juliana.hist"),
        ("Ciências", "marcos.cien"),
        ("Informática", "diogo.info"),
    ]

    materias = []

    for nome_materia, usuario_prof in materias_fixas:
        professor = (
            session.query(Professor)
            .filter(Professor.usuario == usuario_prof)
            .first()
        )

        if not professor:
            logger.error(
                f"Professor com usuário '{usuario_prof}' não encontrado."
            )
            continue

        materias.append(
            Materias(
                nome=nome_materia,
                professor_id=professor.id
            )
        )

    session.add_all(materias)
    session.commit()
    logger.info("Matérias fixas inseridas e vinculadas aos professores.")



# MutantesMaterias 
def seed_mutantes_materias(n: int = 50):
    mutantes_ids = [id[0] for id in session.query(Mutant.id).all()]
    materias_ids = [id[0] for id in session.query(Materias.id).all()]

    if not mutantes_ids or not materias_ids:
        logger.error("Erro: Mutantes ou Matérias ausentes.")
        return

    notas = []
   
    pares_criados = set()

    tentativas = 0
    while len(notas) < n and tentativas < n * 2:
        m_id = random.choice(mutantes_ids)
        mat_id = random.choice(materias_ids)
        
        if (m_id, mat_id) not in pares_criados:
            pares_criados.add((m_id, mat_id))
            
            nova_nota = MutantesMaterias(
                mutante_id=m_id,
                materia_id=mat_id,
                nota1=random.randint(0, 10),
                nota2=random.randint(0, 10),
                observacao=fake.sentence(nb_words=5)
            )
            notas.append(nova_nota)
        tentativas += 1

    session.add_all(notas)
    session.commit()
    logger.info(f"{len(notas)} registros de notas criados!")


def run():
    tasks = [
        (seed_poderes, 10),
        (seed_professores, 0),
        (seed_mutantes, N_ROWS),
        (seed_materias, 0),
        (seed_mutantes_materias, 50)
    ]
    
    try:
        for func, qtd in tasks:
        
            try:
                func(qtd)
                session.commit()
            except Exception as e:
                logger.exception(f"Erro ao executar {func.__name__}:")
                session.rollback()      
    finally:
        session.close()

 
if __name__ == "__main__":
    run()