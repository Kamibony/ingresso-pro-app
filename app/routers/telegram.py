from fastapi import APIRouter, Request, Response
import telegram

# Importa os serviços e a instância central da aplicação
from ..services import chatbot_service
from ..bot import application

router = APIRouter()

# Esta é a função que será chamada para processar as mensagens
async def handle_text_message(update: telegram.Update, context) -> None:
    if update.message and update.message.text:
        chat_id = str(update.message.chat.id)
        user_message = update.message.text
        
        response_text = chatbot_service.processar_mensagem_chatbot(chat_id, user_message)
        
        await update.message.reply_text(response_text)

# Este endpoint apenas recebe a requisição e a encaminha para a biblioteca
@router.post("/telegram/webhook", tags=["Telegram"])
async def telegram_webhook(request: Request):
    """Recebe a atualização do Telegram e a passa para o dispatcher."""
    try:
        update = telegram.Update.de_json(await request.json(), application.bot)
        await application.process_update(update)
    except Exception as e:
        print(f"!!! ERRO NO PROCESSAMENTO DO WEBHOOK: {e} !!!")
    
    return Response(status_code=200)
