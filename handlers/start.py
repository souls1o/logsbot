from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from screens.display import show_main_menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_main_menu(update, context)

def get_handler():
    return CommandHandler('start', start)