from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from screens.display import show_admin_stats

async def adminstats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_admin_stats(update, context)

def get_handler():
    return CommandHandler('adminstats', adminstats)