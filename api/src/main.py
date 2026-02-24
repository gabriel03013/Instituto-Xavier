from typing import Annotated

from auth import User, UserInDB, fake_hash_password, fake_users, get_current_user
from routes.mutant_routes import mutant_router
from routes.teacher_routes import teacher_router
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

load_dotenv()

app = FastAPI()




app.include_router(mutant_router)
app.include_router(teacher_router)


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Authentication Demo"}


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users().get(form_data.username | form_data.email)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username/email or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username/email or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user