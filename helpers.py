import random
import string
from telegram import Update

def get_chat_id(update: Update) -> int:
    return update.message.chat_id if update.message else update.callback_query.message.chat_id

def filter_text(text: str):
    return text.replace('_', '\\_').replace('-', '\\-').replace('.', '\\.').replace('!', '\\!').replace('(', '\\(').replace(')', '\\)').replace('[', '\\[').replace(']', '\\]').replace('=', '\\=').replace('<', '\\<').replace('>', '\\>')
    
def generate_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))