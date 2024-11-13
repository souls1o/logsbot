from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from screens.display import show_main_menu, show_menu, show_account, show_account_logs

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "main_menu":
        await show_main_menu(update, context)
    elif query.data == "menu":
        await show_menu(update, context)
    elif query.data == "account":
        await show_account(update, context)
    elif query.data == "logs_account":
        await show_account_logs(update, context)
    
def get_handler():
    return CallbackQueryHandler(menu_handler)
