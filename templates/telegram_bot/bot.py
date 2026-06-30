import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TOKEN")
async def start(update, ctx): await update.message.reply_text("Hello!")
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
