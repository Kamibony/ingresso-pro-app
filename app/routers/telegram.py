from fastapi import APIRouter, Request, Response
import telegram
from telegram.ext import MessageHandler, filters

# CORREÇÃO: Usando '..' para voltar um nível e encontrar 'services' e 'bot'
from ..services import chatbot_service
from ..bot import application

router = APIRouter()

async def handle_message(update: telegram.Update, context) -> None:
    if update.message and update.message.text:
        chat_id = update.message.chat.id
        user_message = update.message.text
        response_text = chatbot_service.processar_mensagem_chatbot(str(chat_id), user_message)
        await update.message.reply_text(response_text)

application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@router.post("/telegram/webhook", tags=["Telegram"])
async def telegram_webhook(request: Request):
    try:
        update_data = await request.json()
        update = telegram.Update.de_json(update_data, application.bot)
        await application.process_update(update)
    except Exception as e:
        print(f"!!! ERRO NO PROCESSAMENTO DO WEBHOOK: {e} !!!")
    
    return Response(status_code=200)
