from sqlalchemy.orm import Session, sessionmaker
from fastapi import Depends
from database import engine

def get_session():
    try:
        Session = sessionmaker(bind=engine) # Creating connection to database
        session = Session() # Opening an instance of this connection
        yield session # Doesnt finish the func. return and come back here
    finally:
        session.close()