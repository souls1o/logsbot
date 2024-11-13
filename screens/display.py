from collections import defaultdict
from helpers import filter_text, get_emoji
from db import create_user, get_all_users, get_user, create_log, get_all_logs
from keyboards.dynamic import create_account_keyboard, create_main_menu_keyboard, create_menu_keyboard, create_account_logs_keyboard

parse_mode = "MarkdownV2"

async def show_main_menu(update, context):
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name
    reply_markup = create_main_menu_keyboard()
    
    text = f"🔱 *Welcome to __Poseidon Logs__, _{user}_\\!* 🔱\n\n> *ℹ️ Poseidon is the \\#1 and only bot on the market where you can purchase HQ logs seamlessly using various cryptocurrencies such as BTC, ETH, and LTC\\. To get started, add funds from the account menu and search through our menu to find logs that fit your needs\\.*\n\n🔗 *Channel: t\\.me/sheloveosamaa*\n📞 *Support: @fwsouls*"
    await context.bot.send_message(chat_id, text, parse_mode, reply_markup=reply_markup)
    
async def show_menu(update, context):
    chat_id = update.effective_chat.id
    
    # create_log("$15-$20 Balance", 5, 3, "Subway", "Food", "account")
    
    logs_count = sum(len(log.get("logs", [])) for log in get_all_logs())
    reply_markup = create_menu_keyboard(logs_count, 0)
    text = "🚀 *Menu*"
    await context.bot.send_message(chat_id, text, parse_mode, reply_markup=reply_markup)
    
async def show_account_logs(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    logs = get_all_logs()

    product_info = defaultdict(lambda: {"price": float('inf'), "category": None})
    
    for log in logs:
        product = log.get("product")
        category = log.get("category")
        price = log.get("price", float('inf'))

        if product and price < product_info[product]["price"]:
            product_info[product]["price"] = price
            product_info[product]["category"] = category

    products_with_emojis = []
    product_lines = []
    for product, info in product_info.items():
        emoji = get_emoji(info["category"])
        price = info["price"]
        product_text = f"> \\[{emoji}\\] *{product}* \\| 💲*_{price:.2f}_*\\+"
        
        product_lines.append(product_text)
        
        products_with_emojis.append(f"{emoji} {product}")
        
    products_text = "\n".join(product_lines).replace(".", "\\.")
    text = f"📲 *Account Logs*\n\n{products_text}"
    
    reply_markup = create_account_logs_keyboard(products_with_emojis)
    await context.bot.send_message(chat_id, text, parse_mode, reply_markup=reply_markup)
    
async def show_account(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    reply_markup = create_account_keyboard()
    text = "👤 *Account*"
    await context.bot.send_message(chat_id, text, parse_mode, reply_markup=reply_markup)