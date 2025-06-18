# -*- coding: utf-8 -*-
import os
import telegram
from fastapi import APIRouter, Request
from ..services import chatbot_service

router = APIRouter()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "SEU_TOKEN_AQUI")
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

@router.post("/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = telegram.Update.de_json(data, bot)
    if update.message and update.message.text:
        chat_id = update.message.chat_id
        user_message = update.message.text
        bot_response = chatbot_service.processar_mensagem_chatbot(user_message)
        await bot.send_message(chat_id=chat_id, text=bot_response)
    return {"status": "ok"}
