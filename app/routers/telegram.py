from fastapi import APIRouter, Request, Response
import telegram
import os
from app.services import chatbot_service

router = APIRouter()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Variável de ambiente TELEGRAM_BOT_TOKEN não encontrada.")

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

@router.post("/telegram/webhook", tags=["Telegram"])
async def telegram_webhook(request: Request):
    """Recebe as atualizações do Telegram via Webhook."""
    try:
        update_data = await request.json()
        update = telegram.Update.de_json(update_data, bot)
        
        if update.message and update.message.text:
            chat_id = update.message.chat.id
            user_message = update.message.text
            
            response_text = chatbot_service.processar_mensagem_chatbot(str(chat_id), user_message)
            
            await bot.send_message(chat_id=chat_id, text=response_text)
            
    except Exception as e:
        print(f"!!! ERRO NO WEBHOOK DO TELEGRAM: {e} !!!")
    
    return Response(status_code=200)
