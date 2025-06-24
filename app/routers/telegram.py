from fastapi import APIRouter, Request, Response
import telegram
from telegram.ext import MessageHandler, filters
import json # Importar json para ver os dados

from ..services import chatbot_service
from ..bot import application

router = APIRouter()

async def handle_message(update: telegram.Update, context) -> None:
    print("--- 2. Entrou no handle_message ---")
    if update.message and update.message.text:
        chat_id = update.message.chat.id
        user_message = update.message.text
        print(f"--- 3. Recebida mensagem de {chat_id}: '{user_message}' ---")
        
        # Chama o serviço do Gemini para obter a resposta
        response_text = chatbot_service.processar_mensagem_chatbot(str(chat_id), user_message)
        print(f"--- 4. Resposta do Gemini: '{response_text}' ---")
        
        # Envia a resposta de volta para o usuário
        await update.message.reply_text(response_text)
        print("--- 5. Resposta enviada ao usuário. ---")

application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@router.post("/telegram/webhook", tags=["Telegram"])
async def telegram_webhook(request: Request):
    print("--- 1. Webhook do Telegram recebido! ---")
    try:
        update_data = await request.json()
        print("--- Dados recebidos do Telegram (JSON): ---")
        print(json.dumps(update_data, indent=2))

        update = telegram.Update.de_json(update_data, application.bot)
        await application.process_update(update)
    except Exception as e:
        print(f"!!! ERRO CRÍTICO NO WEBHOOK: {e} !!!")
    
    return Response(status_code=200)
