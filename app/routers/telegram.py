from fastapi import APIRouter, Request
import telegram
import os
from services.chatbot_service import ChatbotService

router = APIRouter()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN não encontrado no ambiente.")

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
chatbot_service = ChatbotService()

@router.post("/telegram/webhook", tags=["Telegram"])
async def telegram_webhook(request: Request):
    update_data = await request.json()
    update = telegram.Update.de_json(update_data, bot)
    if update.message and update.message.text:
        chat_id = update.message.chat.id
        user_message = update.message.text
        response_text = chatbot_service.get_response(chat_id, user_message)
        await bot.send_message(chat_id=chat_id, text=response_text)
    return {"status": "ok"}
