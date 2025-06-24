from fastapi import APIRouter, Request, Response
import telegram
from telegram.ext import MessageHandler, filters
import json

from ..services import chatbot_service
from ..bot import application

router = APIRouter()

async def handle_message(update: telegram.Update, context) -> None:
    print("--- PASSO 3: Função 'handle_message' foi ACIONADA! ---")
    if update.message and update.message.text:
        chat_id = update.message.chat.id
        user_message = update.message.text
        print(f"--- PASSO 4: Processando mensagem de {chat_id}: '{user_message}' ---")
        
        response_text = chatbot_service.processar_mensagem_chatbot(str(chat_id), user_message)
        
        print(f"--- PASSO 8: Enviando resposta para o usuário: '{response_text}' ---")
        await update.message.reply_text(response_text)
        print("--- PASSO 9: Resposta enviada com sucesso! FIM DO FLUXO. ---")

# Registra o handler para todas as mensagens de texto que não são comandos
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
print("--- Handler de mensagens registrado na aplicação. ---")

@router.post("/telegram/webhook", tags=["Telegram"])
async def telegram_webhook(request: Request):
    print("--- PASSO 1: Endpoint /telegram/webhook RECEBEU UMA REQUISIÇÃO! ---")
    try:
        update_data = await request.json()
        update = telegram.Update.de_json(update_data, application.bot)
        
        print("--- PASSO 2: Entregando a mensagem para o dispatcher da aplicação... ---")
        await application.process_update(update)
    except Exception as e:
        print(f"!!! ERRO CRÍTICO NO PROCESSAMENTO DO WEBHOOK: {e} !!!")
    
    return Response(status_code=200)
