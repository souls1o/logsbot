from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from screens.display import show_main_menu
from db import update_user

async def ref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    
    code = ""
    if context.args:
        code = context.args[0]
    
    await show_main_menu(update, context)

def get_handler():
    return CommandHandler('ref', ref)