from fastapi import APIRouter, Request, Response
import telegram

from ..services import chatbot_service
from ..bot import application

router = APIRouter()

async def handle_text_message(update: telegram.Update, context) -> None:
    if update.message and update.message.text:
        chat_id = str(update.message.chat.id)
        user_message = update.message.text
        
        response_text = chatbot_service.processar_mensagem_chatbot(chat_id, user_message)
        
        await update.message.reply_text(response_text)

@router.post("/telegram/webhook", tags=["Telegram"])
async def telegram_webhook(request: Request):
    try:
        update = telegram.Update.de_json(await request.json(), application.bot)
        await application.process_update(update)
    except Exception as e:
        print(f"!!! ERRO NO PROCESSAMENTO DO WEBHOOK: {e} !!!")
    
    return Response(status_code=200)
