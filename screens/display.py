from collections import defaultdict
from helpers import filter_text, get_emoji
from db import create_user, get_all_users, get_user, create_log, get_log, get_all_logs, create_order, get_order, get_all_orders
from keyboards.dynamic import create_account_keyboard, create_main_menu_keyboard, create_menu_keyboard, create_account_logs_keyboard, create_orders_keyboard

parse_mode = "MarkdownV2"

async def show_main_menu(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    reply_markup = create_main_menu_keyboard()
    text = f"🔱 *Welcome to __Poseidon Logs__, _{user_name}_\\!* 🔱\n\n> *ℹ️ Poseidon is the \\#1 and only bot on the market where you can purchase HQ logs seamlessly using various cryptocurrencies such as BTC, ETH, and LTC\\. To get started, add funds from the account menu and search through our menu to find logs that fit your needs\\.*\n\n📢 *\\| t\\.me/sheloveosamaa*\n📞 *\\| @fwsouls*"
    
    user = get_user(user_id)
    if not user:
        create_user(user_id)
    
    if context.user_data.get("message_id"):
        await context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data["message_id"], text=text, parse_mode=parse_mode, reply_markup=reply_markup)
    else:
        message = await context.bot.send_message(chat_id, text, parse_mode, reply_markup=reply_markup)
        context.user_data["message_id"] = message.message_id
        
async def show_menu(update, context):
    chat_id = update.effective_chat.id
    message_id = context.user_data["message_id"]
    
    # create_log("Coinbase FA", 6.00, 4.00, "FA (Hotmail)", "FA", "account")
    
    logs_count = sum(len(log.get("logs", [])) for log in get_all_logs())
    reply_markup = create_menu_keyboard(logs_count, 0)
    text = "🚀 *Menu*\n\nChoose an option:"
    await context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data["message_id"], text=text, parse_mode=parse_mode, reply_markup=reply_markup)
    
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
        product = filter_text(product)
        product_text = f"> *\\[{emoji}\\] {product} \\| $_{price:.2f}_*\\+"
        
        product_lines.append(product_text)
        
        product = product.replace("\\", "")
        products_with_emojis.append(f"{emoji} {product}")
        
    products_text = "\n".join(product_lines).replace(".", "\\.")
    text = f"📲 *Account Logs*\n\n{products_text}"
    
    reply_markup = create_account_logs_keyboard(products_with_emojis)
    await context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data["message_id"], text=text, parse_mode=parse_mode, reply_markup=reply_markup)
    
async def show_account(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = context.user_data["message_id"]
    
    user = get_user(user_id)
    orders = user["orders"]
    
    spent = 0.00
    for order_id in orders:
        order = get_order(order_id)
        log_id = order["info"]["log_id"]
        
        log = get_log(log_id)
        spent += log["price"]
    
    balance = user["balance"]
    order_count = len(orders)
    
    reply_markup = create_account_keyboard()
    text = f"👤 *Account*\n\n> 💲 *Balance:* $_{balance:.2f}_\n> 🛒 *Total Spent:* $_{spent:.2f}_\n> 📦 *Total Orders:* _{order_count}_".replace(".", "\\.")
    await context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data["message_id"], text=text, parse_mode=parse_mode, reply_markup=reply_markup)
    
async def show_orders(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = context.user_data["message_id"]
    
    user = get_user(user_id)
    orders = user["orders"]
    order_texts = []
    
    for i, order_id in enumerate(orders, start=1):
        order = get_order(order_id)
        order_id = order["order_id"]
        log_id = order["info"]["log_id"]
        
        log = get_log(log_id)
        name = log["name"]
        product = log["product"]
        price = log["price"]
        emoji = get_emoji(log["category"])
        
        timestamp = order["timestamp"]
        order_text = (
            f"> \\[_{i}_\\] {emoji} *{product} \\| {name}*\n"
            f"> \\[_{log_id}_\\] *$_{price:.2f}_*"
            f"> \\[_{order_id}_\\] 🕐 `{timestamp}`"
        )
        order_texts.append(order_text)
    
    orders_text = "\n\n".join(order_texts).replace(".", "\\.").replace("(", "\\(").replace(")", "\\)")
    text = f"📦 *Order History*\n\n{orders_text}\n\n📦 *Total Orders:* __"
    
    reply_markup = create_orders_keyboard()
    await context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data["message_id"], text=text, parse_mode=parse_mode, reply_markup=reply_markup)