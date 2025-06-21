from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente IMEDIATAMENTE
load_dotenv()

# Agora, importa os módulos do projeto
from database import engine
from routers import telegram, dashboard, testing
from models import database_models

# Tenta criar as tabelas no banco de dados
try:
    print("Tentando criar tabelas do banco de dados...")
    database_models.Base.metadata.create_all(bind=engine)
    print("Tabelas do banco de dados verificadas/criadas com sucesso.")
except Exception as e:
    print(f"ERRO AO CONECTAR/CRIAR TABELAS DO BANCO DE DADOS: {e}")

app = FastAPI(
    title="Concierge Pro Platform",
    description="API para conectar clientes a prestadores de serviço.",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(telegram.router)
app.include_router(dashboard.router)
app.include_router(testing.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bem-vindo à API Concierge Pro!"}
