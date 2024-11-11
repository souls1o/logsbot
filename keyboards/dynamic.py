from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🚀 Menu", callback_data="menu")],
        [InlineKeyboardButton("👤 Account", callback_data="account")]
    ]
    return InlineKeyboardMarkup(keyboard)
    
def create_menu_keyboard(logs_count, banks_count):
    keyboard = [
        [InlineKeyboardButton(f"📲 Account Logs ({logs_count})", callback_data="logs_account")],
        [InlineKeyboardButton(f"🏦 Bank Logs ({banks_count})", callback_data="logs_bank")]
    ]
    return InlineKeyboardMarkup(keyboard)
    
def create_account_logs_keyboard():
    keyboard = [
        [InlineKeyboardButton("📂 Orders", callback_data="orders")],
        [InlineKeyboardButton("💳 Add Funds", callback_data="deposit")],
        [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)
    
def create_account_keyboard():
    keyboard = [
        [InlineKeyboardButton("📂 Orders", callback_data="orders")],
        [InlineKeyboardButton("💳 Add Funds", callback_data="deposit")],
        [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)