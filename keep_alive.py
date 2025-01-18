import requests
from flask import Flask, request
from threading import Thread
from db import get_user, update_user, get_transaction, create_transaction, update_transaction

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
    confimations = data["confirmations"]
    
    transactions = get_all_transactions()
    
    transaction = next((tx for tx in transactions if tx["info"]["txid"] == txid), None)
    if transaction:
        if transaction["status"] != "confirmed" and confirmations >= 1:
            user = get_user(user_id)
            user["balances"][currency] += value/100000000
            user["transactions"].append(transaction["transaction_id"])
            update_user(user_id, user)
            
            transaction["status"] = "confirmed"
            update_transaction(transaction["transaction_id"], transaction)
    else:
        create_transaction(user_id, value, currency, txid)
    
def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()
