from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from screens.display import show_ref_stats

async def refstats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_red_stats(update, context)

def get_handler():
    return CommandHandler('refstats', refstats)