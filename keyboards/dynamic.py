import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def create_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🚀 Menu", callback_data="menu")],
        [InlineKeyboardButton("👤 Account", callback_data="account")],
        [InlineKeyboardButton("🛒 Cart", callback_data="cart")]
    ]
    return InlineKeyboardMarkup(keyboard)
    
def create_menu_keyboard(logs_count, banks_count):
    keyboard = [
        [InlineKeyboardButton(f"📲 Account Logs ({logs_count})", callback_data="logs_account")],
        [InlineKeyboardButton(f"🏦 Bank Logs ({banks_count})", callback_data="logs_bank")],
        [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)
    
def create_account_logs_keyboard(products):
    keyboard = []
    row = []
        
    for i, product in enumerate(products):
        product_data = re.sub(r'[^A-Za-z]', '', product).lower().replace(' ', '_')
        row.append(InlineKeyboardButton(product, callback_data=f"product_{product_data}"))
        
        if (i + 1) % 2 == 0:
            keyboard.append(row)
            row = []
            
    if row:
        keyboard.append(row)
        
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="menu")])
    
    return InlineKeyboardMarkup(keyboard)
    
def create_account_keyboard():
    keyboard = [
        [InlineKeyboardButton("📂 Orders", callback_data="orders")],
        [InlineKeyboardButton("💳 Add Funds", callback_data="deposit")],
        [InlineKeyboardButton("⬅️ Back", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)
    
def create_deposit_keyboard():
    keyboard = [
        [InlineKeyboardButton("BTC", callback_data="deposit_btc")],
        [InlineKeyboardButton("ETH", callback_data="deposit_eth")],
        [InlineKeyboardButton("LTC", callback_data="deposit_ltc")],
        [InlineKeyboardButton("⬅️ Back", callback_data="account")]
    ]
    return InlineKeyboardMarkup(keyboard)