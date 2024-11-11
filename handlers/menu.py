from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from screens.display import show_menu, show_account_logs

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "logs_account":
        await show_account_logs(update, context)
    
def get_handler():
    return CallbackQueryHandler(menu_handler)