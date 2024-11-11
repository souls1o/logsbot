from keyboards.dynamic import create_account_keyboard, create_main_menu_keyboard, create_menu_keyboard 

parse_mode = "MarkdownV2"

async def show_main_menu(update, context):
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name
    reply_markup = create_main_menu_keyboard()
    
    text = f"🔱 *Welcome to __POSEIDON__, _{user}_\\!* 🔱\n\n* ℹ️ Poseidon is the \\#1 and only bot on the market where you can purchase HQ logs seamlessly using various cryptocurrencies such as BTC, ETH, and LTC\\. To get started, add funds from the account menu and search through our menu to find logs that fit your needs\\.*\n\n📞 *Support: @fwsouls*"
    await context.bot.send_message(chat_id, text, parse_mode, reply_markup)
    
async def show_menu(update, context):
    chat_id = update.effective_chat.id
    reply_markup = create_menu_keyboard()
    
    text = "🚀 *Menu*"
    await context.bot.send_message(chat_id, text, parse_mode, reply_markup)
    
async def show_account(update, context):
    chat_id = update.effective_chat.id
    reply_markup = create_menu_keyboard()
    
    text = "👤 *Account*"
    await context.bot.send_message(chat_id, text, parse_mode, reply_markup)