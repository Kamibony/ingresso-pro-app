# app/bot.py
import os
from telegram.ext import Application

# Pega o token do ambiente
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Variável de ambiente TELEGRAM_BOT_TOKEN não foi definida.")

# Cria a aplicação usando o padrão builder (o jeito moderno e correto)
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
