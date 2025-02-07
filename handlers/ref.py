from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from screens.display import show_main_menu
from db import get_user, update_user

async def ref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    
    if not context.args:
        return
        
    user = get_user(update.effective_user.id)
        
    code = context.args[0]
    if code == "test":
        user["ref"] = 7434895838
        update_user(update.effective_user.id, user)
    
    await show_main_menu(update, context)

def get_handler():
    return CommandHandler('ref', ref)