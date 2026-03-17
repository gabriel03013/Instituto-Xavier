"""
Main com todas as rotas do projeto, unificando e identificando suas funções e eventos
"""

__author__ = ["Gustavo Manganelli", "Erik Santos", "Gabriel Mendes"]

from typing import Annotated

from sqlalchemy.orm import Session
from routes.user_routes import user_router
from dependencies import get_session
from auth_utils import listar_mutantes as mutantes, listar_professores as professores, verificar_adm, verificar_usuario
from db.helpers.security import verify_password
from routes.mutante_routes import mutante_router
from routes.professor_routes import professor_router
from routes.observacao_routes import observacao_router
from routes.turma_routes import turma_router
from routes.mutante_materia_routes import mutante_materia_router
from routes.materia_routes import materia_router
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from routes.admin_routes import admin_router
from routes.tarefa_routes import tarefa_router
from routes.recovery_routes import recovery_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_router)
app.include_router(mutante_router)
app.include_router(professor_router)
app.include_router(user_router)
app.include_router(observacao_router)
app.include_router(turma_router)
app.include_router(mutante_materia_router)
app.include_router(materia_router)
app.include_router(tarefa_router)
app.include_router(recovery_router)


@app.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session = Depends(get_session)):
    user_obj = None
    identificador = None

    if verificar_usuario(form_data.username):
        for m in mutantes(session):
            if m.email == form_data.username:
                user_obj = m
                identificador = m.email
                break
    else:
        for p in professores(session):
            if p.usuario == form_data.username:
                user_obj = p
                identificador = p.usuario
                break

    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, user_obj.senha):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if verificar_adm(form_data.username):
        tipo = "ADMIN"
    elif verificar_usuario(form_data.username):
        tipo = "MUTANTE"
    else:
        tipo = "PROFESSOR"
    
    materia_id = None
    if tipo == "PROFESSOR" and user_obj.materias:
        materia_id = user_obj.materias[0].id

    return {
        "access_token": identificador, 
        "token_type": "bearer",
        "tipo": tipo,
        "id": user_obj.id,
        "materia_id": materia_id
    }