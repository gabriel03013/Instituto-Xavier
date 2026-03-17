"""
Template HTML para email de recuperação de senha.
"""


def gerar_email_html(token: str, mutante_nome: str, frontend_url: str) -> str:
    """Gera corpo HTML do email de recuperação."""
    reset_link = f"{frontend_url}/pages/admin/recuperacao.html?token={token}"
    
    return f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);">
                <h2 style="color: #333;">Olá, {mutante_nome}!</h2>
                
                <p style="color: #666; line-height: 1.6;">
                    Recebemos uma solicitação para redefinir sua senha no <strong>Instituto Xavier</strong>.
                </p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_link}" style="background-color: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">
                        Redefinir Senha
                    </a>
                </div>
                
                <p style="color: #999; font-size: 12px; margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px;">
                    Este link expira em 1 hora.
                </p>
            </div>
        </body>
    </html>
    """