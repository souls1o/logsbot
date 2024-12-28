import random
import string
from telegram import Update

def get_chat_id(update: Update) -> int:
    return update.message.chat_id if update.message else update.callback_query.message.chat_id

def filter_text(text: str):
    return text.replace('_', '\\_').replace('-', '\\-').replace('.', '\\.').replace('!', '\\!').replace('(', '\\(').replace(')', '\\)').replace('[', '\\[').replace(']', '\\]').replace('=', '\\=').replace('<', '\\<').replace('>', '\\>')
    
def escape_markdown(text: str):
    chars = r"[]()<>+-|.!#"
    for char in chars:
        text = text.replace(char, f"\\{char}")
    return text
    
def generate_id(n: int):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))
    
def get_emoji(category):
    category_emojis = {
        "Food": "🍔",
        "FA": "🔓",
        "Shopping": "🛍️"
    }
    
    return category_emojis.get(category, "❓")
    
def get_product(product):
    products = {
        "fa_hotmail": "FA (Hotmail)",
        "subway": "Subway",
        "starbucks_gc_no_pin": "Starbucks <GC NO-PIN>",
        "starbucks": "Starbucks"
    }
    
    return products.get(product, "❓")
    
def emojify(number):
    digit_to_emoji = {
        '0': '0️⃣',
        '1': '1️⃣',
        '2': '2️⃣',
        '3': '3️⃣',
        '4': '4️⃣',
        '5': '5️⃣',
        '6': '6️⃣',
        '7': '7️⃣',
        '8': '8️⃣',
        '9': '9️⃣',
    }
    return ''.join(digit_to_emoji[digit] for digit in str(number))