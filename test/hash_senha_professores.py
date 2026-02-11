from db.helpers.security import hash_password
import os 
from dotenv import load_dotenv

load_dotenv()

SENHA_PROFESSORES = os.getenv("SENHA_PROFESSORES")

senha = hash_password(SENHA_PROFESSORES)
print(f"Senha hash: {senha}")

