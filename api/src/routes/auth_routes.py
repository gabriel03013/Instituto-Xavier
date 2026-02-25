from typing import Annotated

from auth import User, UserInDB, fake_hash_password, fake_users, get_current_user
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/")
async def root():
    return {"message": "Welcome to FastAPI Authentication Demo"}


@auth_router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user
