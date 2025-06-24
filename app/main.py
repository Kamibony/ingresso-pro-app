from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
import os
from telegram.ext import MessageHandler, filters

# Importa a instância 'application' e os routers
from .bot import application
from .routers import telegram, dashboard, testing

# Importa a função que lida com as mensagens
from .routers.telegram import handle_text_message

app = FastAPI(title="Concierge Pro Platform")

@app.on_event("startup")
async def startup_event():
    # Registra o handler de mensagens durante a inicialização
    # Isso garante que a aplicação saiba o que fazer com as mensagens de texto
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text_message))
    
    # Configura o webhook do Telegram
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        raise ValueError("Variável de ambiente WEBHOOK_URL não foi definida.")
    
    await application.bot.set_webhook(url=f"{webhook_url}/telegram/webhook")
    print("Handler de mensagens registrado e webhook configurado com sucesso.")

@app.on_event("shutdown")
async def shutdown_event():
    await application.bot.delete_webhook()
    print("Webhook removido.")

# Inclui as rotas da sua API
app.include_router(telegram.router)
app.include_router(dashboard.router)
app.include_router(testing.router)

@app.get("/")
def read_root():
    return {"status": "Concierge Pro API online!"}
