from collections import defaultdict
from helpers import escape_markdown, get_emoji, emojify, get_product
from db import create_user, get_all_users, get_user, create_log, get_log, get_all_logs, create_order, get_order, get_all_orders
from keyboards.dynamic import create_account_keyboard, create_main_menu_keyboard, create_menu_keyboard, create_account_logs_keyboard, create_orders_keyboard, create_order_keyboard

parse_mode = "MarkdownV2"

async def show_main_menu(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    reply_markup = create_main_menu_keyboard()
    text = f"🔱 *Welcome to __Poseidon__, _{user_name}_\\!* 🔱\n\n> *ℹ️ Poseidon is the \\#1 bot on the market where you can purchase HQ logs seamlessly using various cryptocurrencies such as BTC, ETH, and LTC\\. To get started, add funds from the account menu and search through our menu to find logs that fit your needs\\.*\n\n📢 *\\| t\\.me/diablosgrave*\n💬 *\\| t\\.me/fraudschemin*\n📞 *\\| @fwsouls*"
    
    user = get_user(user_id)
    if not user:
        create_user(user_id)
    
    if context.user_data.get("message_id"):
        await context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data["message_id"], text=text, parse_mode=parse_mode, reply_markup=reply_markup, disable_web_page_preview=True)
    else:
        message = await context.bot.send_message(chat_id, text, parse_mode, reply_markup=reply_markup, disable_web_page_preview=True)
        context.user_data["message_id"] = message.message_id
        
async def show_menu(update, context):
    chat_id = update.effective_chat.id
    message_id = context.user_data["message_id"]
    
    # create_log("$5-$10 Giftcard", 1.25, 0.65, "Starbucks", "Food", "account")
    
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
        product_text = f"> *[{emoji}] {product} | $_{price:.2f}_*+"
        
        product_lines.append(product_text)
        products_with_emojis.append(f"{emoji} {product}")
        
    products_text = "\n".join(product_lines)
    text = escape_markdown(f"👥 *Account Logs*\n\n{products_text}")
    
    reply_markup = create_account_logs_keyboard(products_with_emojis)
    await context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data["message_id"], text=text, parse_mode=parse_mode, reply_markup=reply_markup)
    
async def show_options(update, context, product):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = context.user_data["message_id"]
    
    user = get_user(user_id)
    product = get_product(product)
    logs = get_all_logs()
    log_texts = []
    
    for log in logs:
        log_product = log.get("product")
        if log_product == product:
            log_id = log.get("log_id")
            log_name = log.get("name")
            log_price = log.get("price")
            global cat_emoji
            cat_emoji = get_emoji(log.get("category"))
            
            log_texts.append(f"> {cat_emoji} *$__{log_price:.2f}__ | {log_name}*\n> #️⃣ _{log_id}_")
            
    logs_display = "\n\n".join(log_texts)
    text = escape_markdown(f"{cat_emoji} *{product}\n\n{logs_display}")
    await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode=parse_mode)
    
async def show_account(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = context.user_data["message_id"]
    
    user = get_user(user_id)
    orders = user["orders"]
    
    spent = 0.00
    for order_id in orders:
        order = get_order(order_id)
        logs = order["info"]["log_ids"]
        
        for log_id in logs:
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
    order_count = len(orders)
    order_texts = []
    
    for i, order_id in enumerate(orders, start=1):
        order = get_order(order_id)
        order_id = order["order_id"]
        logs = order["info"]["log_ids"]
        timestamp = order["timestamp"].strftime("%Y-%m-%d %H:%M")
        cost = 0.00
        
        log_infos = {}
        for log_id in logs:
            log = get_log(log_id)
            cost += log["price"]
            if log_id not in log_infos:
                log_infos[log_id] = {"quantity": 0, "price": log["price"], "name": log["name"], "product": log["product"], "emoji": get_emoji(log["category"])}
            else:
                log_infos[log_id]["price"] += log["price"]
            log_infos[log_id]["quantity"] += 1
            
        log_texts = []
        log_values = list(log_infos.values())
        for log_info in log_values[:3]:
            name = log_info["name"]
            product = log_info["product"]
            emoji = log_info["emoji"]
            quantity = log_info["quantity"]
            price = log_info["price"]
            log_texts.append(f"> {emoji} *{product} | {name} - x*_{quantity}_ ($__{price:.2f}__)")
        
        extra = len(log_values) - 3
        if extra > 0:
            total = sum(log_info["price"] for log_info in log_values[3:])
            logs_display = "\n".join(log_texts) + f"\n> ➕ *{extra} MORE* ($__{total:.2f}__)"
        else:
            logs_display = "\n".join(log_texts)
            
        order_text = (
            f"[*_{i}_*] *{order_id} — $_{cost:.2f}_*\n"
            f"{logs_display}\n"
            f"> *[* 🕐 _{timestamp}_ *]*"
        )
        order_texts.append(order_text)
    
    no_orders = "> _Nothing to see here... 👀_"
    orders_text = "\n\n".join(order_texts)
    text = escape_markdown(f"📦 *Order History*\n\n{orders_text if orders else no_orders}\n\n📦 *Total Orders:* {order_count}")
    
    reply_markup = create_orders_keyboard(orders)
    await context.bot.edit_message_text(chat_id=chat_id, message_id=context.user_data["message_id"], text=text, parse_mode=parse_mode, reply_markup=reply_markup)
    
async def show_order(update, context, order_id):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_id = context.user_data["message_id"]
    
    order = get_order(order_id)
    logs = order["info"]["log_ids"]
    timestamp = order["timestamp"].strftime("%Y-%m-%d %H:%M")
    total = len(logs)
    cost = 0.00
    
    log_infos = {}
    for log_id in logs:
        log = get_log(log_id)
        cost += log["price"]
        if log_id not in log_infos:
            log_infos[log_id] = {"quantity": 0, "price": log["price"], "name": log["name"], "product": log["product"], "emoji": get_emoji(log["category"])}
        else:
            log_infos[log_id]["price"] += log["price"]
        log_infos[log_id]["quantity"] += 1

    log_values = sorted(log_infos.values(), key=lambda x: x["price"], reverse=True)

    log_texts = []
    for log_info in log_values:
        name = log_info["name"]
        product = log_info["product"]
        emoji = log_info["emoji"]
        quantity = log_info["quantity"]
        price = log_info["price"]
        log_texts.append(f"> {emoji} *{product} | {name} - x*_{quantity}_ ($__{price:.2f}__)")
        
    logs_display = "\n".join(log_texts)
    
    text = escape_markdown(f"📦 *Order #__{order_id}__\n\nℹ️ __Details:__*\n> 💰 *Cost: $_{cost:.2f}_*\n> #️⃣ *Count: __{total}__*\n> 🕐 `{timestamp}`\n\n👤 *__Logs:__*\n{logs_display}")
    reply_markup = create_order_keyboard(order_id)
    await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode=parse_mode, reply_markup=reply_markup)