from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
import os
from telegram.ext import MessageHandler, filters

from .bot import application
from .routers import telegram, dashboard, testing
from .routers.telegram import handle_text_message

app = FastAPI(title="Concierge Pro Platform")

@app.on_event("startup")
async def startup_event():
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text_message))
    
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        raise ValueError("Variável de ambiente WEBHOOK_URL não foi definida.")
    
    await application.bot.set_webhook(url=f"{webhook_url}/telegram/webhook")
    print("Handler de mensagens registrado e webhook configurado.")

@app.on_event("shutdown")
async def shutdown_event():
    await application.bot.delete_webhook()
    print("Webhook removido.")

app.include_router(telegram.router)
app.include_router(dashboard.router)
app.include_router(testing.router)

@app.get("/")
def read_root():
    return {"status": "Concierge Pro API online!"}
