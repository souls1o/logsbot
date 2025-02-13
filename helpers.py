import random
import string
import requests
from telegram import Update

def get_chat_id(update: Update) -> int:
    return update.message.chat_id if update.message else update.callback_query.message.chat_id

def filter_text(text: str):
    return text.replace('_', '\\_').replace('-', '\\-').replace('.', '\\.').replace('!', '\\!').replace('(', '\\(').replace(')', '\\)').replace('[', '\\[').replace(']', '\\]').replace('=', '\\=').replace('<', '\\<').replace('>', '\\>')
    
def escape_markdown(text: str):
    chars = r"[]()<+-|.!#"
    for char in chars:
        text = text.replace(char, f"\\{char}")
    return text
    
def generate_id(n: int):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))
    
def get_emoji(category):
    category_emojis = {
        "Coffee": "☕️",
        "Pizza": "🍕",
        "FA": "🔓",
        "Mail": "✉️",
        "Shopping": "🛍️"
    }
    
    return category_emojis.get(category, "❓")
    
def get_product(product):
    products = {
        "hotmailfa": "Hotmail (FA)",
        "dominos": "Dominos",
        "subway": "Subway",
        "starbucksgcnopin": "Starbucks <GC NO-PIN>",
        "starbucks": "Starbucks"
    }
    
    return products.get(product, "❓")
    
def generate_address(user_id, ticker):
    payload = {
      "currency": ticker,
      "callback": {
        "method": "POST",
        "url": "https://logsbot-irmb.onrender.com/callback",
        "data": {
          "user_id": user_id
        }
      }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    res = requests.post("https://apirone.com/api/v2/accounts/apr-e4ee22c85068e9fbf7f7f66b27775edd/addresses", json=payload, headers=headers)
    if res.status_code == 200:
        data = res.json()
        return data["address"]
        
def get_prices():
    """Fetch the current USD price for BTC and LTC."""
    url = f"https://api.coincap.io/v2/assets?ids=bitcoin,litecoin"
    headers = { "Authorization": "Bearer 2123650e-a596-4647-85af-ec374e18af35" }
    response = requests.get(url, headers=headers)
    data = response.json()["data"]
    
    return float(data[0]["priceUsd"]), float(data[1]["priceUsd"])