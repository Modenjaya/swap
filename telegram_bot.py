from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
import asyncio
from config import TELEGRAM_BOT_TOKEN

class TelegramBot:
    def __init__(self):
        self.app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        self.app.add_handler(CommandHandler("start", self.start))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Halo! Bot Solana Copy Trading siap berjalan.")

    def run(self):
        print("Telegram Bot started...")
        self.app.run_polling()
