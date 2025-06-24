from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
import os
from telegram.ext import MessageHandler, filters

# Importa a instância da aplicação e os routers
from .bot import application
from .routers import telegram, dashboard, testing

# Importa a função específica que queremos registrar
from .routers.telegram import handle_message

app = FastAPI(title="Concierge Pro Platform")

@app.on_event("startup")
async def startup_event():
    # Registra o handler de mensagens durante a inicialização
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Configura o webhook
    webhook_url = os.getenv("WEBHOOK_URL")
    await application.bot.set_webhook(url=f"{webhook_url}/telegram/webhook")
    print("Handler de mensagens registrado e webhook configurado.")

@app.on_event("shutdown")
async def shutdown_event():
    await application.bot.delete_webhook()
    print("Webhook removido.")

# Inclui os routers
app.include_router(telegram.router)
app.include_router(dashboard.router)
app.include_router(testing.router)

@app.get("/")
def read_root():
    return {"status": "Concierge Pro API online!"}
