import psycopg2 as psy
from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv("HOST")
DB = os.getenv("DB")
USER= os.getenv("USER")
PASSWORD= os.getenv("PASSWORD")
PORT= os.getenv("PORT")

try:
    con = psy.connect(
        host = HOST,
        database = DB,
        user = USER,
        password = PASSWORD,
        port = PORT 
    )

    cur = con.cursor()

    cur.execute("SELECT * FROM alunos")
    con.commit()
    
except psy.OperationalError:
    print("Conexão recusada")