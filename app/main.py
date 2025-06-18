# -*- coding: utf-8 -*-
from fastapi import FastAPI
from dotenv import load_dotenv

# A SOLUÇÃO: Carrega as variáveis de ambiente ANTES de qualquer outro import da nossa aplicação.
load_dotenv()

# Agora, importa os outros módulos que dependem dessas variáveis.
from .models import database_models
from .database import engine
from .routers import dashboard, telegram, testing

# Cria as tabelas no banco de dados
database_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Concierge Pro API")

# Inclui os routers no nosso aplicativo principal
app.include_router(dashboard.router, tags=["Dashboard"])
app.include_router(telegram.router, prefix="/webhook", tags=["Telegram"])
app.include_router(testing.router, prefix="/api", tags=["Testing"])


@app.get("/", summary="Endpoint raiz")
def read_root():
    """Verifica se o servidor está online."""
    return {"status": "Servidor do Concierge Pro está online!"}
