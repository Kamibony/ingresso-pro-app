from fastapi import APIRouter, Request, Response
import telegram
from telegram.ext import MessageHandler, filters

from ..services import chatbot_service
from ..bot import application

router = APIRouter()

# Esta é a função que será chamada para lidar com as mensagens
async def handle_text_message(update: telegram.Update, context) -> None:
    # Verifica se a mensagem de fato contém texto
    if update.message and update.message.text:
        chat_id = str(update.message.chat.id)
        user_message = update.message.text
        
        print(f"MENSAGEM RECEBIDA [ChatID: {chat_id}]: {user_message}")
        
        # Chama o serviço do Gemini para obter a resposta
        response_text = chatbot_service.processar_mensagem_chatbot(chat_id, user_message)
        
        print(f"RESPOSTA GERADA [ChatID: {chat_id}]: {response_text}")
        
        # Envia a resposta de volta para o usuário
        await update.message.reply_text(response_text)
        print(f"RESPOSTA ENVIADA [ChatID: {chat_id}]")

# Registra a função acima como o "handler" de mensagens
# Usando um filtro simples para qualquer texto que não seja um comando
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text_message))


# Este endpoint apenas recebe a requisição e a entrega para a biblioteca
@router.post("/telegram/webhook", tags=["Telegram"])
async def telegram_webhook(request: Request):
    """Recebe a atualização do Telegram e a passa para o dispatcher."""
    try:
        update_data = await request.json()
        update = telegram.Update.de_json(update_data, application.bot)
        await application.process_update(update)
    except Exception as e:
        print(f"!!! ERRO NO PROCESSAMENTO DO WEBHOOK: {e} !!!")
    
    return Response(status_code=200)
