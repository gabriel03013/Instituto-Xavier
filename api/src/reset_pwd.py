from database import Session
from models import Mutante
from db.helpers.security import hash_password
import os

session = Session()

try:
    mutante = session.query(Mutante).filter(Mutante.email == "19552@instituto.com").first()
    if mutante:
        mutante.senha = hash_password("123456")
        session.commit()
        print(f"Senha resetada para o usuário {mutante.nome}")
    else:
        print("Usuário não encontrado")
except Exception as e:
    print(f"Erro: {e}")
finally:
    session.close()
