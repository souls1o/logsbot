import requests
from flask import Flask, request
from threading import Thread
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
    currency = data["currency"]
    txid = data["input_transaction_hash"]
    confirmations = data["confirmations"]
    
    transactions = get_all_transactions()
    
    transaction = next((tx for tx in transactions if tx["info"]["txid"] == txid), None)
    if transaction:
        if transaction["status"] != "confirmed" and confirmations >= 1:
            user = get_user(user_id)
            amount = value/100000000
            user["balances"][currency] += amount
            user["transactions"].append(transaction["transaction_id"])
            update_user(user_id, user)
            
            transaction["status"] = "confirmed"
            update_transaction(transaction["transaction_id"], transaction)
            
            curr_up = currency.upper()
            message = (
              f"✅ *Payment Confirmed*\n\n"
              f"_Your payment of *{amount} {curr_up}* has successfully confirmed._"
            )
            
            payload = {
              "chat_id": user_id,
              "text": message,
              "parse_mode": "MarkdownV2"
            }
            
            requests.post("https://api.telegram.org/bot7845815456:AAE3qpHwyUj21VX32_k4XiwoajLVGsxxdBc/sendMessage", json=payload)
    else:
        create_transaction(user_id, value, currency, txid)
        
        message = (
          f"🔄 *Payment Pending*\n\n"
          f"_Your payment of *{amount} {curr_up}* is pending._"
        )
            
        payload = {
          "chat_id": user_id,
          "text": message,
          "parse_mode": "MarkdownV2"
        }
            
        requests.post("https://api.telegram.org/bot7845815456:AAE3qpHwyUj21VX32_k4XiwoajLVGsxxdBc/sendMessage", json=payload)
        
    return {"status": "received"}, 200
    
def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()
