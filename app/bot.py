import os
from telegram.ext import Application

# Pega o token do ambiente
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# --- Log de Depuração ---
if TELEGRAM_BOT_TOKEN:
    print(f"Token do Telegram encontrado! Começa com: {TELEGRAM_BOT_TOKEN[:8]}...")
else:
    print("!!! ATENÇÃO: Variável de ambiente TELEGRAM_BOT_TOKEN não foi encontrada!!!")
    raise ValueError("Variável de ambiente TELEGRAM_BOT_TOKEN não foi definida.")

# Cria a aplicação usando o padrão builder
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
