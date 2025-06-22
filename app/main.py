from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import engine
from routers import telegram, dashboard, testing
from models import database_models

try:
    print("Tentando criar tabelas do banco de dados...")
    database_models.Base.metadata.create_all(bind=engine)
    print("Tabelas do banco de dados verificadas/criadas com sucesso.")
except Exception as e:
    print(f"ERRO AO INICIALIZAR O BANCO DE DADOS: {e}")
    raise

app = FastAPI(title="Concierge Pro Platform")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(telegram.router)
app.include_router(dashboard.router)
app.include_router(testing.router)

@app.get("/")
def read_root():
    return {"status": "API online"}
