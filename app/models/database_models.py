# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, JSON
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
    observacao = Column(String)
