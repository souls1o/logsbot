from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from db import get_user, update_user
from screens.display import show_main_menu, show_menu, show_account, show_orders, show_order, show_account_logs, show_options, show_logs_file, show_deposit, show_deposit_addr, show_option

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "main_menu":
        await show_main_menu(update, context)
    elif query.data == "menu":
        await show_menu(update, context)
    elif query.data == "account":
        await show_account(update, context)
    elif query.data == "orders":
        await show_orders(update, context)
    elif query.data == "depo":
        await show_deposit(update, context)
    elif query.data == "logs_account":
        await show_account_logs(update, context)
    elif query.data.startswith("deposit_"):
        ticker = query.data.split("_", 1)[1]
        await show_deposit_addr(update, context, ticker)
    elif query.data.startswith("product_"):
        product = query.data.split("_", 1)[1]
        await show_options(update, context, product)
    elif query.data.startswith("order_"):
        order_id = query.data.split("_", 1)[1]
        await show_order(update, context, order_id)
    elif query.data.startswith("logs_"):
        order_id = query.data.split("_", 1)[1]
        await show_logs_file(update, context, order_id)
    elif query.data.startswith("option_"):
        log_id = query.data.split("_", 1)[1]
        await show_option(update, context, log_id)
    elif query.data.startswith("add_cart_"):
        log_id = query.data.split("_", 1)[2]
        
        user = get_user(update.effective_user.id)
        user["cart"].append(log_id)
        update_user(update.effective_user.id, user)
        
        await show_option(update, context, log_id)
    elif query.data.startswith("remove_cart_"):
        log_id = query.data.split("_", 1)[2]
        
        user = get_user(update.effective_user.id)
        if log_id in user["cart"]:
            user["cart"].remove(log_id)
            update_user(update.effective_user.id, user)
        
        await show_option(update, context, log_id)
    
def get_handler():
    return CallbackQueryHandler(menu_handler)
