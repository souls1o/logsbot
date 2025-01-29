import requests
from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes
from db import get_user, update_user, get_log
from screens.display import show_main_menu, show_menu, show_account, show_orders, show_order, show_account_logs, show_options, show_logs_file, show_deposit, show_deposit_addr, show_option, show_cart
from helpers import get_price

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
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
    elif query.data == "cart":
        await show_cart(update, context)
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
        log_id = query.data.split("cart_", 1)[1]
        
        user = get_user(update.effective_user.id)
        user["cart"].append(log_id)
        update_user(update.effective_user.id, user)
        
        await show_option(update, context, log_id)
    elif query.data.startswith("remove_cart_"):
        log_id = query.data.split("cart_", 1)[1]
        
        user = get_user(update.effective_user.id)
        if log_id in user["cart"]:
            user["cart"].remove(log_id)
            update_user(update.effective_user.id, user)
        
        await show_option(update, context, log_id)
    elif query.data.startswith("purchase"):
        user = get_user(update.effective_user.id)
        cost = sum(get_log(log_id)["price"] for log_id in user["cart"])
            
        btc_balance = user["balances"].get("btc")
        ltc_balance = user["balances"].get("ltc")
        
        btc_usd = btc_balance * get_price("btc") if btc_balance else 0
        ltc_usd = ltc_balance * get_price("ltc") if ltc_balance else 0
        total_usd = btc_usd + ltc_usd
        
        if total_usd < cost:
            await query.answer("❌ Insufficient balance", show_alert=True)
            return
            
        half_cost = cost / 2
        
        btc_used = min(half_cost, btc_usd)
        remaining = half_cost - btc_used
        
        ltc_used = min(half_cost + remaining, ltc_usd)
        
        if ltc_used < (half_cost + remaining):
            btc_used += (half_cost + remaining) - ltc_used
            
        btc_deducted = btc_used / btc_price if btc_price else 0
        ltc_deducted = ltc_used / ltc_price if ltc_price else 0
    
        user["balances"]["btc"] -= btc_deducted
        user["balances"]["ltc"] -= ltc_deducted
        
        update_user(update.effective_user.id, user)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Purchase successful!")
    
def get_handler():
    return CallbackQueryHandler(menu_handler)
