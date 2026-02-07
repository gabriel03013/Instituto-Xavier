from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DB_URI")


engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

Base = declarative_base()