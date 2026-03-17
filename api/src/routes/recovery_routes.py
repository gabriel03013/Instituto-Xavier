"""
Rotas para recuperação de senha de mutantes e professores.

Oferece endpoints para solicitar recuperação de senha e redefinir senha
através de token JWT.
"""

__author__ = "Davi Franco"


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependencies import get_session
from auth_utils import listar_mutantes, listar_professores, verificar_usuario, verificar_adm
from services.recovery_service import RecoveryService
from schemas.recovery_schema import RecoveryRequest, ResetPasswordRequest
from dao.mutante_dao import MutanteDAO
from dao.professor_dao import ProfessorDAO
from db.helpers.security import hash_password

recovery_router = APIRouter(prefix="/auth", tags=["recovery"])
recovery_service = RecoveryService()


@recovery_router.post("/recuperar-senha")
async def recuperar_senha(
    request: RecoveryRequest,
    session: Session = Depends(get_session)
) -> dict:
    """
    Solicita recuperação de senha para mutante ou professor.
    
    Busca o usuário pelo email/usuário fornecido, gera um token JWT
    e envia email com link de recuperação.
    
    Args:
        request (RecoveryRequest): Requisição contendo email/usuário.
        session (Session): Sessão do banco de dados.
        
    Returns:
        dict: Mensagem de confirmação.
        
    Raises:
        HTTPException: Se houver erro ao enviar email.
    """
    try:
        email_input = request.email
        usuario = None
        tipo = None
        
        # Tenta buscar mutante
        if verificar_usuario(email_input):
            for m in listar_mutantes(session):
                if m.email == email_input:
                    usuario = m
                    tipo = "mutante"
                    break
        
        # Tenta buscar professor
        if not usuario:
            for p in listar_professores(session):
                if p.usuario == email_input:
                    usuario = p
                    tipo = "professor"
                    break
        
        # Segurança: não revela se usuário existe
        if not usuario:
            return {"msg": "Se o email/usuário existe, você receberá um link."}
        
        # Gera token e envia email
        token = recovery_service.gerar_token(usuario.id, usuario.email if tipo == "mutante" else usuario.usuario, tipo)
        recovery_service.enviar_email(
            destinatario=usuario.email if tipo == "mutante" else usuario.email,
            nome=usuario.nome,
            token=token,
            tipo=tipo
        )
        
        return {"msg": "Email enviado com sucesso."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@recovery_router.post("/redefinir-senha")
async def redefinir_senha(
    request: ResetPasswordRequest,
    session: Session = Depends(get_session)
) -> dict:
    """
    Redefinir senha de mutante ou professor.
    
    Valida o token JWT, verifica se as senhas conferem e atualiza
    a senha no banco de dados.
    
    Args:
        request (ResetPasswordRequest): Requisição contendo token e nova senha.
        session (Session): Sessão do banco de dados.
        
    Returns:
        dict: Mensagem de confirmação.
        
    Raises:
        HTTPException: Se token inválido, senhas não conferirem, etc.
    """
    try:
        # Valida token
        payload = recovery_service.validar_token(request.token)
        
        # Valida senhas
        if request.nova_senha != request.confirmar_senha:
            raise ValueError("Senhas não conferem")
        
        if len(request.nova_senha) < 6:
            raise ValueError("Senha deve ter no mínimo 6 caracteres")
        
        usuario_id = payload["usuario_id"]
        tipo = payload["tipo"]
        
        # Atualiza senha no banco
        hashed_password = hash_password(request.nova_senha)
        if tipo == "mutante":
            MutanteDAO(session=session).atualizar(usuario_id, senha=hashed_password)
        else:
            ProfessorDAO(session=session).atualizar(usuario_id, senha=hashed_password)
        
        return {"msg": "Senha redefinida com sucesso."}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))