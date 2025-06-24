import os
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from telegram.ext import MessageHandler, filters

# Carrega as variáveis de ambiente
load_dotenv()

from .bot import application
from .database import engine
from .models import database_models
from .routers import dashboard, telegram as telegram_router, testing
from .routers.telegram import handle_text_message

# Cria as tabelas no banco de dados (se não existirem)
database_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Concierge Pro API",
    description="API para conectar clientes a prestadores de serviço.",
    version="1.0.0"
)

# Configura templates
app.state.templates = Jinja2Templates(directory="app/templates")

# Adiciona o handler do Telegram diretamente na aplicação
# Isso garante que ele esteja registrado antes do webhook ser configurado.
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text_message))

@app.on_event("startup")
async def startup_event():
    """Configura o webhook do Telegram na inicialização."""
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        print("AVISO: WEBHOOK_URL não definida. O webhook não será configurado.")
        return
    
    await application.bot.set_webhook(
        url=f"{webhook_url}/telegram/webhook",
        allowed_updates=telegram.Update.ALL_TYPES
    )
    print(f"Webhook configurado para: {webhook_url}/telegram/webhook")

@app.on_event("shutdown")
async def shutdown_event():
    """Remove o webhook do Telegram no desligamento."""
    print("Removendo webhook...")
    await application.bot.delete_webhook()

# Inclui os roteadores da aplicação
app.include_router(dashboard.router, tags=["Dashboard"])
app.include_router(telegram_router.router, tags=["Telegram"])
app.include_router(testing.router, tags=["Testing"])

@app.get("/", summary="Endpoint raiz da API", include_in_schema=False)
def read_root():
    return {"status": "API do Concierge Pro está no ar!"}
