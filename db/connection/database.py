from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# a URI ta como postgresql+psycopg pq o aiven exige o uso do psycopg2, e o SQLAlchemy precisa dessa especificação pra 
# usar o driver certo. Se fosse só postgresql, ele tentaria usar o driver padrão (psycopg) que é mais recente, mas não 
# é compatível com a versão do PostgreSQL que a Aiven oferece. Então, pra garantir que a conexão funcione, a gente tem 
# que especificar o driver na URI.
DATABASE_URL = os.getenv("DB_URI")


engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()