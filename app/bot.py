import os
from telegram.ext import Application

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Variável de ambiente TELEGRAM_BOT_TOKEN não foi definida.")

application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
