from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🚀 Menu", callback_data="menu")],
        [InlineKeyboardButton("👤 Account", callback_data="account")]
    ]
    return InlineKeyboardMarkup(keyboard)
    
def create_menu_keyboard(menu_items):
    keyboard = [
        [InlineKeyboardButton("🚀 Menu", callback_data="menu")],
        [InlineKeyboardButton("👤 Account", callback_data="account")]
    ]
    return InlineKeyboardMarkup(keyboard)
    
def create_account_keyboard():
    keyboard = [
        [InlineKeyboardButton("📂 Orders", callback_data="orders")],
        [InlineKeyboardButton("💳 Add Funds", callback_data="deposit")],
        [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)