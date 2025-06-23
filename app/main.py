# app/main.py
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

# Importa a instância da aplicação do nosso novo arquivo
from .bot import application
from .routers import telegram, dashboard, testing

app = FastAPI(title="Concierge Pro Platform")

@app.on_event("startup")
async def startup_event():
    """
    No momento em que a aplicação inicia, esta função é chamada.
    Ela configura o webhook do Telegram.
    """
    # Pega a URL do serviço a partir de uma variável de ambiente
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        raise ValueError("Variável de ambiente WEBHOOK_URL não foi definida.")
        
    # Usa a instância 'application' para configurar o webhook
    await application.bot.set_webhook(url=f"{webhook_url}/telegram/webhook")
    print(f"Webhook configurado para: {webhook_url}/telegram/webhook")

@app.on_event("shutdown")
async def shutdown_event():
    """Ao desligar, remove o webhook."""
    await application.bot.delete_webhook()
    print("Webhook removido.")


app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Inclui os routers
app.include_router(telegram.router)
app.include_router(dashboard.router)
app.include_router(testing.router)

@app.get("/")
def read_root():
    return {"status": "Concierge Pro API online!"}
