from sqlalchemy import Column, Integer, String, JSON, Text, DateTime
from sqlalchemy.sql import func
from ..database import Base

class Prestador(Base):
    __tablename__ = "prestadores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    telefone = Column(String)
    categoria = Column(String, index=True)
    especialidades = Column(JSON)
    bairro = Column(String)
    disponibilidade = Column(String)
    observacao = Column(String, nullable=True)

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True)
    session_id = Column(String, index=True, nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
