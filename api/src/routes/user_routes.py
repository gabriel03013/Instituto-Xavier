from typing import Annotated
from fastapi import APIRouter, Depends
from auth import User, get_current_user

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user
