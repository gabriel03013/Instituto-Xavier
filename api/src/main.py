from typing import Annotated

from auth import User, UserInDB, fake_hash_password, fake_users, get_current_user
from routes.mutante_routes import mutante_router
from routes.professor_routes import professor_router
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

load_dotenv()

app = FastAPI()

from routes.admin_routes import admin_router
from routes.mutante_routes import mutante_router
from routes.professor_routes import professor_router
from routes.auth_routes import auth_router


app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(mutante_router)
app.include_router(professor_router)

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users().get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username/email or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username/email or password")

    return {"access_token": user.username, "token_type": "bearer"}