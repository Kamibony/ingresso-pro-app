# app/routers/telegram.py
from fastapi import APIRouter, Request, Response
import telegram
from telegram.ext import MessageHandler, filters

from app.services import chatbot_service
from ..bot import application  # Importa a instância centralizada

router = APIRouter()

# 1. ESTA É A FUNÇÃO QUE EXECUTA QUANDO UMA MENSAGEM CHEGA
async def handle_message(update: telegram.Update, context) -> None:
    """Processa a mensagem de texto recebida do usuário."""
    if update.message and update.message.text:
        chat_id = update.message.chat.id
        user_message = update.message.text
        
        # Chama o serviço do Gemini para obter a resposta
        response_text = chatbot_service.processar_mensagem_chatbot(str(chat_id), user_message)
        
        # Envia a resposta de volta para o usuário
        await update.message.reply_text(response_text)

# 2. AQUI REGISTRAMOS A FUNÇÃO ACIMA COMO O "HANDLER" DE MENSAGENS DE TEXTO
# A biblioteca irá chamar handle_message sempre que receber um texto que não seja um comando.
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


# 3. ESTE ENDPOINT APENAS RECEBE A REQUISIÇÃO DO TELEGRAM E A ENTREGA PARA A APLICAÇÃO
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
