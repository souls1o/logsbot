import random
import string
from telegram import Update

def get_chat_id(update: Update) -> int:
    return update.message.chat_id if update.message else update.callback_query.message.chat_id

def filter_text(text: str):
    return text.replace('_', '\\_').replace('-', '\\-').replace('.', '\\.').replace('!', '\\!').replace('(', '\\(').replace(')', '\\)').replace('[', '\\[').replace(']', '\\]').replace('=', '\\=').replace('<', '\\<').replace('>', '\\>')
    
def escape_markdown(text: str):
    chars = r"[]()+-|.!"
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