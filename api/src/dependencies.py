from sqlalchemy.orm import Session, sessionmaker
from fastapi import Depends
from database import engine
import psycopg2
import os

HOST=os.getenv("HOST")
DATABASE=os.getenv("DATABASE")
USER=os.getenv("USER")
PASSWORD=os.getenv("PASSWORD")

def get_session():
    conn = None
    cursor = None
    
    try: 
        conn = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD
        )

        cursor = conn.cursor()
        yield cursor
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# def get_session():
#     try:
#         Session = sessionmaker(bind=engine) # Creating connection to database
#         session = Session() # Opening an instance of this connection
#         yield session # Doesnt finish the func. return and come back here
#     finally:
#         session.close()