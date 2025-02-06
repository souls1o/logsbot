from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def add_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 7863772639:
        return

    if not context.args:
        return await update.message.reply_text("Usage: /add_stock <log_id>")

    context.bot_data["awaiting_file"] = True
    context.bot_data["log_id"] = context.args[0]
    await update.message.reply_text("Send the stock file")

def get_handler():
    return CommandHandler('add_stock', add_stock)