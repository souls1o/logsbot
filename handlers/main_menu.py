from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from screens.display import show_menu, show_account

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "menu":
        await show_menu(update, context)
    elif query.data == "account":
        await show_account(update, context)
    
def get_handler():
    return CallbackQueryHandler(main_menu_handler)