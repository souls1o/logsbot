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
        "orders": [],
        "timestamp": datetime.utcnow()
    }
    try:
        users.insert_one(user_data)
        print(f'[+] User ')
    except Exception as e:
        print(f"[-] Failed to create user: {e}")
        
def create_log(name, price, cost, product, category, type):
    log_id = generate_id()
    
    log_data = {
        "log_id": log_id,
        "name": name,
        "price": price,
        "cost": cost,
        "product": product,
        "category": category,
        "type": type,
        "logs": [],
        "timestamp": datetime.utcnow()
    }
    try:
        logs.insert_one(log_data)
        print(f'[+] Log created: {log_id} ')
    except Exception as e:
        print(f"[-] Failed to create log: {e}")

        
def get_user(user_id):
    try:
        return users.find_one({"user_id": user_id})
    except Exception as e:
        print(f"[-] Failed to retrieve user: {e}")
        return Non
        
def get_all_users():
    try:
        return list(users.find())
    except Exception as e:
        print(f"[-] Failed to retrieve all users: {e}")
        return []
        
def update_user(user_id, user_data):
    try:
        result = users.update_one(
            {"user_id": user_id},
            {"$set": user_data}
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"[-] Failed to update user: {e}")
        return False
        
def get_all_logs():
    try:
        return list(logs.find())
    except Exception as e:
        print(f"[-] Failed to retrieve all logs: {e}")
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