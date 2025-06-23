# app/routers/telegram.py
from fastapi import APIRouter, Request, Response
import telegram
from app.services import chatbot_service

# Importa a instância da aplicação do nosso novo arquivo
from ..bot import application

router = APIRouter()

@router.post("/telegram/webhook", tags=["Telegram"])
async def telegram_webhook(request: Request):
    """
    Este endpoint recebe as atualizações do Telegram e as processa.
    """
    try:
        update_data = await request.json()
        update = telegram.Update.de_json(update_data, application.bot)

        # A forma correta de passar a atualização para a biblioteca processar
        await application.process_update(update)

    except Exception as e:
        print(f"!!! ERRO NO WEBHOOK DO TELEGRAM: {e} !!!")
    
    return Response(status_code=200)


# O MessageHandler agora intercepta qualquer mensagem de texto
@application.message_handler(None)
async def message_handler(update: telegram.Update, context) -> None:
    """
    Este é o handler que efetivamente processa a mensagem do usuário.
    """
    if update.message and update.message.text:
        chat_id = update.message.chat.id
        user_message = update.message.text
        
        # Chama o serviço do Gemini para obter a resposta
        response_text = chatbot_service.processar_mensagem_chatbot(str(chat_id), user_message)
        
        # Envia a resposta de volta para o usuário
        await update.message.reply_text(response_text)
