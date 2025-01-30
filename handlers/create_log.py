from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from screens.display import show_log_creation

async def create_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_log_creation(update, context)

def get_handler():
    return CommandHandler('create_log', create_log)