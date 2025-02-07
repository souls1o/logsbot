import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from helpers import generate_id
from datetime import datetime

client = MongoClient(os.environ["MONGO_URI"], server_api=ServerApi('1'))
db = client["db"]
users = db["users"]
logs = db["logs"]
orders = db["orders"]
transactions = db["transactions"]
infos = db["infos"]

def test_connection():
    try:
        client.admin.command('ping')
        print("[+] MongoDB has successfully connected.")
    except Exception as e:
        print("[-] MongoDB has failed to connect.")
        print(e)
        
def create_user(user_id):
    user_data = {
        "user_id": user_id,
        "ref": 7434895838,
        "addresses": {
            "btc": "",
            "ltc": ""
        },
        "balances": {
            "btc": 0.00,
            "ltc": 0.00
        },
        "commission": 0.00,
        "transactions": [],
        "cart": [],
        "orders": [],
        "timestamp": datetime.utcnow()
    }
    try:
        users.insert_one(user_data)
        print(f'[+] User ')
    except Exception as e:
        print(f"[-] Failed to create user: {e}")
        
def create_log(name, desc, price, cost, product, category, filename, type):
    log_id = generate_id(6)
    
    log_data = {
        "log_id": log_id,
        "name": name,
        "desc": desc,
        "price": price,
        "cost": cost,
        "product": product,
        "category": category,
        "filename": filename,
        "type": type,
        "logs": [],
        "timestamp": datetime.utcnow()
    }
    try:
        logs.insert_one(log_data)
        print(f'[+] Log created: {log_id} ')
    except Exception as e:
        print(f"[-] Failed to create log: {e}")

def create_order(user_id, paid, cost, log_ids, logs):
    order_data = {
        "order_id": generate_id(8),
        "paid": paid,
        "cost": cost,
        "costs": 0.00,
        "info": {
            "user_id": user_id,
            "log_ids": log_ids,
            "logs": logs
        },
        "timestamp": datetime.utcnow()
    }
    try:
        orders.insert_one(order_data)
        return order_data
        print(f'[+] Order ')
    except Exception as e:
        print(f"[-] Failed to create order: {e}")
        return Nons
        
def create_transaction(user_id, value, currency, txid):
    transaction_data = {
        "transaction_id": generate_id(10),
        "status": "pending",
        "info": {
            "user_id": user_id,
            "value": value,
            "currency": currency,
            "txid": txid
        },
        "timestamp": datetime.utcnow()
    }
    try:
        transactions.insert_one(transaction_data)
        print(f'[+] Transaction ')
    except Exception as e:
        print(f"[-] Failed to create transaction: {e}")

        
def update_user(user_id, data):
    try:
        return users.update_one({"user_id": user_id}, {"$set": data})
    except Exception as e:
        print(f"[-] Failed to update user: {e}")
        return None
        
def update_log(log_id, data):
    try:
        return logs.update_one({"log_id": log_id}, {"$set": data})
    except Exception as e:
        print(f"[-] Failed to update log: {e}")
        return None
        
def update_transaction(transaction_id, data):
    try:
        return transactions.update_one({"transaction_id": transaction_id}, {"$set": data})
    except Exception as e:
        print(f"[-] Failed to update transaction: {e}")
        return None
        
def get_user(user_id):
    try:
        return users.find_one({"user_id": user_id})
    except Exception as e:
        print(f"[-] Failed to retrieve user: {e}")
        return None
        
def get_log(log_id):
    try:
        return logs.find_one({"log_id": log_id})
    except Exception as e:
        print(f"[-] Failed to retrieve log: {e}")
        return None
        
def get_order(order_id):
    try:
        return orders.find_one({"order_id": order_id})
    except Exception as e:
        print(f"[-] Failed to retrieve order: {e}")
        return None
        
def get_transaction(transaction_id):
    try:
        return transactions.find_one({"transaction_id": transaction_id})
    except Exception as e:
        print(f"[-] Failed to retrieve transaction: {e}")
        return None
        
def get_all_users():
    try:
        return list(users.find())
    except Exception as e:
        print(f"[-] Failed to retrieve all users: {e}")
        return []
        
def get_all_logs():
    try:
        return list(logs.find())
    except Exception as e:
        print(f"[-] Failed to retrieve all logs: {e}")
        return []
        
def get_all_orders():
    try:
        return list(orders.find())
    except Exception as e:
        print(f"[-] Failed to retrieve all orders: {e}")
        return []
        
def get_all_transactions():
    try:
        return list(transactions.find())
    except Exception as e:
        print(f"[-] Failed to retrieve all transactions: {e}")
        return []

def create_or_update_user(user_id, user_data):
    try:
        result = users.update_one(
            {"user_id": user_id},
            {"$set": user_data},
            upsert=True
        )
        if result.upserted_id:
            print(f"[+] User created with ID: {result.upserted_id}")
        else:
            print(f"[+] User {user_id} updated successfully.")
        return True
    except Exception as e:
        print(f"[-] Failed to create or update user: {e}")
        return False
    
def create_info(info_id, title, description, category):
    info_data = {
        "info_id": info_id,
        "title": title,
        "desc": description,
        "category": category,
        "timestamp": datetime.utcnow()
    }
    try:
        infos.insert_one(info_data)
        print(f'[+] Info {info_id} created with title "{title}" in {category}')
    except Exception as e:
        print(f"[-] Failed to create info: {e}")