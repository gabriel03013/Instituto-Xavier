import smtplib
from email.message import EmailMessage
from enum import Enum
from dataclasses import dataclass
from dotenv import load_dotenv
import os
from typing import TypedDict

load_dotenv()

@dataclass
class EmailConfig:
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587  
    sender_email: str = "institutoxavier@gmail.com"
    password: str = os.getenv("SENHA_EMAIL")


class Mailer:
    def __init__(self, config: EmailConfig):
        self.config = config

    def send(self, to_email: str, subject: str, body: str):
        msg = EmailMessage()
        
        msg['Subject'] = subject
        msg['From'] = self.config.sender_email
        msg['To'] = to_email
        msg.set_content(body)

        with smtplib.SMTP(self.config.smtp_server, self.config.smtp_port) as server:
            server.starttls() 
            server.login(self.config.sender_email, self.config.password)
            server.send_message(msg)

