import psycopg2 as psy
from dotenv import load_dotenv
import os

load_dotenv()

def get_sql(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

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
        
    create = get_sql("sql/create.sql")
    dataload = get_sql("sql/dataload.sql")
    view = get_sql("sql/view.sql")
    
    cur.execute(create)
    cur.execute(dataload)
    cur.execute(view)
    
    con.commit()
    
    cur.close()
    con.close()
  
except FileNotFoundError:
    print("Arquivo não encontrado")
    
except psy.OperationalError:
    print("Conexão recusada")

print("Script executado!")