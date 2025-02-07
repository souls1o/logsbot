from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from screens.display import show_main_menu
from db import get_user, update_user, create_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    
    if context.args:
        user_id = update.effective_user.id
        user = get_user(user_id)
        if not user:
            user = create_user(user_id)
            if context.args[0] == "test":
                user["ref"] = 7863772639
                update_user(user_id, user)
    
    await show_main_menu(update, context)

def get_handler():
    return CommandHandler('start', start)