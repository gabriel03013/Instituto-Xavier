"""
Schemas para recuperação de senha de mutantes e professores.

__author__ = "Davi Franco"
"""

from pydantic import BaseModel


class RecoveryRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    nova_senha: str
    confirmar_senha: str