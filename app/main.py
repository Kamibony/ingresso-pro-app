from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from .bot import application
from .routers import telegram, dashboard, testing

app = FastAPI(title="Concierge Pro Platform")

@app.on_event("startup")
async def startup_event():
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        raise ValueError("Variável de ambiente WEBHOOK_URL não foi definida.")
    
    await application.bot.set_webhook(url=f"{webhook_url}/telegram/webhook")
    print(f"Webhook configurado para: {webhook_url}/telegram/webhook")

@app.on_event("shutdown")
async def shutdown_event():
    await application.bot.delete_webhook()
    print("Webhook removido.")

# A linha abaixo foi removida para corrigir o erro de inicialização
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(telegram.router)
app.include_router(dashboard.router)
app.include_router(testing.router)

@app.get("/")
def read_root():
    return {"status": "Concierge Pro API online!"}
