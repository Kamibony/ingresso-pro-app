import os
import telegram
from fastapi import APIRouter, Request, Response
from sqlalchemy.orm import Session
from fastapi.params import Depends

from ..bot import application
from ..services import chatbot_service
from ..database import get_db

router = APIRouter()

async def handle_text_message(update: telegram.Update, context: telegram.ext.ContextTypes.DEFAULT_TYPE):
    """Processa a mensagem de texto recebida e responde."""
    chat_id = update.message.chat_id
    message_text = update.message.text
    
    # Obtém uma sessão de banco de dados do contexto
    # A sessão será injetada no contexto pelo process_update
    db_session: Session = context.bot_data["db_session"]
    
    response_text = chatbot_service.generate_response(
        session_id=str(chat_id),
        message=message_text,
        db=db_session
    )
    
    await context.bot.send_message(chat_id=chat_id, text=response_text)

@router.post("/telegram/webhook", include_in_schema=False)
async def telegram_webhook(request: Request, db: Session = Depends(get_db)):
    """Recebe as atualizações do Telegram via webhook."""
    try:
        # Coloca a sessão do banco de dados no contexto do bot
        # para que o handler possa usá-la.
        application.bot_data["db_session"] = db
        
        update = telegram.Update.de_json(await request.json(), application.bot)
        await application.process_update(update)
    except Exception as e:
        print(f"!!! ERRO NO PROCESSAMENTO DO WEBHOOK: {e} !!!")
    
    return Response(status_code=200)
