"""
Rota para recuperar o usuário autenticado.
"""

__author__ = "Gustavo Manganelli"

from typing import Annotated
from fastapi import APIRouter, Depends
from auth import User, get_current_user

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """
    Retorna as informações do usuário atualmente autenticado.

    Args:
        current_user (User): Usuário extraído do token via dependência.

    Returns:
        User: Objeto de usuário autenticado.
    """
    return current_user
