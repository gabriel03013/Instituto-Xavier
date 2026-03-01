from typing import Annotated

from sqlalchemy.orm import Session
from routes.user_routes import user_router
from dependencies import get_session
from auth_utils import listar_mutantes as mutantes, listar_professores as professores, verificar_usuario
from db.helpers.security import verify_password
from routes.mutante_routes import mutante_router
from routes.professor_routes import professor_router
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

load_dotenv()

app = FastAPI()

from routes.admin_routes import admin_router
from routes.mutante_routes import mutante_router
from routes.professor_routes import professor_router


app.include_router(admin_router)
app.include_router(mutante_router)
app.include_router(professor_router)
app.include_router(user_router)

@app.post("/token")
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
    return {"access_token": identificador, "token_type": "bearer"}