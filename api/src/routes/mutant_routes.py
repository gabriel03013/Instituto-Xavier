from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.mutantSchema import MutantSchema
from dependencies import get_session
from database import engine

mutant_router = APIRouter(prefix="/student", tags=["student"])


@mutant_router.get("/")
async def home():
    return {"msg": "Welcome, student!"}


@mutant_router.post("/register_mutant")
async def criar(
    mutant_schema: MutantSchema
):
    return {"msg": mutant_schema}


@mutant_router.get("/try_connection")
async def get_connection_test(session: Session = Depends(get_session)):
    
    # TODO verify if connection to database is working
    # session.query(Mutantes)

    print(session)