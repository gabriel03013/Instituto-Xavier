from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas.mutantSchema import MutantCreate, MutantSchema
from dependencies import get_session
from database import engine
from models import Professor

mutant_router = APIRouter(prefix="/student", tags=["student"])


@mutant_router.get("/")
async def home():
    return {"msg": "Welcome, student!"}


@mutant_router.post("/register_mutant")
async def criar(
    mutant_schema: MutantCreate
):
    return {"msg": mutant_schema}


@mutant_router.get("/try_connection")
async def get_connection_test(session: Session = Depends(get_session)):
    
    # TODO verify if connection to database is working
    # session.query(Mutantes)

    print(session)


@mutant_router.get("/see_mutants")
async def see_mutants(
    id: int,
    session: Session = Depends(get_session)
):
    
    mutants = session.query(Professor).filter(Professor.id==id).first()

    return {"msg": mutants}