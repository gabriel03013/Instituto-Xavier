from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from schemas.mutantesSchema import MutanteSchema
from dependencies import get_session
from database import engine
from dependencies import get_session
from models import Mutante


mutante_router = APIRouter(prefix="/mutant", tags=["mutant"])


@mutante_router.get("/")
async def home():
    return {"msg": "Welcome, mutant!"}


@mutante_router.get("/health_db")
async def health_db(session: Session = Depends(get_session)):
    """"
    Try connection with database just executing a simple select then returns successful or failure.
    """
    try:
        session.execute(text("SELECT 1"))
        return {"status": "Database connection successful"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )


# -- CREATE --
@mutante_router.post("/register_mutante")
async def register_mutante(
    mutante_schema: MutanteSchema,
    session: Session = Depends(get_session)
):
    new_mutante = Mutante(**mutante_schema.model_dump())
    
    session.add(new_mutante)
    session.commit()
    session.refresh(new_mutante)

    return {"msg": f"New Mutante inserted successfuly! ID: {new_mutante.id}"}


# -- READ --
@mutante_router.get("/list")
async def list_mutantes(
    session: Session = Depends(get_session)
):
    session.query(Mutante).all()

    return {
        "mutantes": Mutante
    }


@mutante_router.get("/find_mutante")
async def find_mutante(
    id: int,
    session: Session = Depends(get_session)
):
    
    mutante = session.query(Mutante).filter(Mutante.id==id).first()

    if not mutante:
        raise HTTPException(statuscode=401, detail="Couldn't find any Mutante by that ID.")

    return {"mutante": mutante}