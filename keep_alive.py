import requests
from flask import Flask, request
from threading import Thread
from helpers import get_prices
from db import get_user, update_user, get_transaction, create_transaction, update_transaction, get_all_transactions

app = Flask(__name__)

@app.route('/')
def index():
  return "Alive"

@app.route('/callback', methods=['POST'])
def callback():
    data = request.json
    user_id = data["data"]["user_id"]
    value = data["value"]
    amount = value/100000000
    currency = data["currency"]
    txid = data["input_transaction_hash"]
    confirmations = data["confirmations"]
    
    transactions = get_all_transactions()
    
    curr_up = currency.upper()
    
    transaction = next((tx for tx in transactions if tx["info"]["txid"] == txid), None)
    if transaction:
        if transaction["status"] != "confirmed" and confirmations >= 1:
            user = get_user(user_id)
            user["balances"][currency] += amount
            user["transactions"].append(transaction["transaction_id"])
            update_user(user_id, user)
            
            transaction["status"] = "confirmed"
            update_transaction(transaction["transaction_id"], transaction)
            
            btc_price, ltc_price = get_prices()
            usd_amount = amount * (ltc_price if currency == "ltc" else btc_price)
            
            message = (
              f"✅ *Payment Confirmed*\n\n"
              f"_Your payment of $*{usd_amount:.2f}* (*{amount} {curr_up}*) has successfully confirmed._"
            ).replace(".", "\\.")
            
            payload = {
              "chat_id": user_id,
              "text": message,
              "parse_mode": "MarkdownV2"
            }
            
            requests.post("https://api.telegram.org/bot7603587678:AAHvRhm7eMVpOj-jG3sLhDeEamjrnwt-GFU/sendMessage", json=payload)
    else:
        create_transaction(user_id, value, currency, txid)
        
        btc_price, ltc_price = get_prices()
        usd_amount = amount * (ltc_price if currency == "ltc" else btc_price)
        
        message = (
          f"🔄 *Payment Pending*\n\n"
          f"_Your payment of $*{usd_amount:.2f}* (*{amount} {curr_up}*) is pending._"
        ).replace(".", "\\.")
            
        payload = {
          "chat_id": user_id,
          "text": message,
          "parse_mode": "MarkdownV2"
        }
            
        requests.post("https://api.telegram.org/bot7603587678:AAHvRhm7eMVpOj-jG3sLhDeEamjrnwt-GFU/sendMessage", json=payload)
        
    return {"status": "received"}, 200
    
def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()
