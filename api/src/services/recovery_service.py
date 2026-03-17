"""
Service para gerenciamento de recuperação de senha.

Responsável por geração de tokens JWT, validação de tokens e envio de emails
para mutantes e professores.
"""

__author__ = "Davi Franco"


import jwt
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "chave_segura")
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRY_MINUTES = 60


class RecoveryService:
    """
    Service para gerenciar recuperação de senha.
    
    Fornece métodos para gerar tokens JWT, validar tokens e enviar
    emails de recuperação para mutantes e professores.
    """
    
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SENDER_PASSWORD = os.getenv("SENHA_EMAIL")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5500")
    
    def gerar_token(self, usuario_id: int, email: str, tipo: str) -> str:
        """
        Gera um token JWT para recuperação de senha.
        
        Args:
            usuario_id (int): ID do mutante ou professor.
            email (str): Email do mutante ou usuário do professor.
            tipo (str): Tipo de usuário ("mutante" ou "professor").
            
        Returns:
            str: Token JWT codificado e assinado.
            
        Raises:
            ValueError: Se tipo for inválido.
        """
        if tipo not in ("mutante", "professor"):
            raise ValueError(f"Tipo inválido: {tipo}")
        
        payload = {
            "usuario_id": usuario_id,
            "email": email,
            "tipo": tipo,
            "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRY_MINUTES)
        }
        
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    def validar_token(self, token: str) -> dict:
        """
        Valida um token JWT e extrai o payload.
        
        Args:
            token (str): Token JWT a validar.
            
        Returns:
            dict: Payload decodificado contendo usuario_id, email e tipo.
            
        Raises:
            ValueError: Se token expirou ou for inválido.
        """
        try:
            return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expirado")
        except jwt.InvalidTokenError:
            raise ValueError("Token inválido")
    
    def enviar_email(self, destinatario: str, nome: str, token: str, tipo: str) -> None:
        """
        Envia email de recuperação de senha.
        
        Args:
            destinatario (str): Email do destinatário.
            nome (str): Nome do mutante ou professor.
            token (str): Token JWT para inclusão no link.
            tipo (str): Tipo de usuário ("mutante" ou "professor").
            
        Returns:
            None
            
        Raises:
            Exception: Se houver erro ao enviar email.
        """
        try:
            link = f"{self.FRONTEND_URL}/pages/admin/recuperacao.html?token={token}"
            
            msg = EmailMessage()
            msg['Subject'] = "Instituto Xavier - Recuperar Senha"
            msg['From'] = self.SENDER_EMAIL
            msg['To'] = destinatario
            
            corpo = f"""
            <html>
                <body style="font-family: Arial; background-color: #f4f4f4; padding: 20px;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px;">
                        <h2>Olá, {nome}!</h2>
                        <p>Recebemos uma solicitação para redefinir sua senha no Instituto Xavier.</p>
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{link}" style="background-color: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">
                                Redefinir Senha
                            </a>
                        </div>
                        <p style="color: #999; font-size: 12px; margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px;">
                            Este link expira em 60 minutos.
                        </p>
                    </div>
                </body>
            </html>
            """
            
            msg.set_content("Clique no link do email para recuperar sua senha.")
            msg.add_alternative(corpo, subtype='html')
            
            with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
                server.starttls()
                server.login(self.SENDER_EMAIL, self.SENDER_PASSWORD)
                server.send_message(msg)
        
        except Exception as e:
            raise Exception(f"Erro ao enviar email: {str(e)}")