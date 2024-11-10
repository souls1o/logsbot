import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(os.environ["MONGO_URI"], server_api=ServerApi('1'))
db = client["db"]
users = db["users"]
logs = db["logs"]

def test_db_connection():
    try:
        client.admin.command('ping')
        print("[+] MongoDB has successfully connected.")
    except Exception as e:
        print("[-] MongoDB has failed to connect.")
        print(e)
        
def get_user(user_id):
    try:
        return users.find_one({"user_id": user_id})
    except Exception as e:
        print(f"[-] Failed to retrieve user: {e}")
        return None
        
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
        
def get_all_users():
    try:
        return list(users.find())
    except Exception as e:
        print(f"[-] Failed to retrieve all users: {e}")
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
    
def create_log(log_id, title, description, category):):
    log_data = {
        "log_id": log_id,
        "title": title,
        "desc": description,
        "category": category,
        "timestamp": datetime.utcnow()
    }
    try:
        logs.insert_one(log_data)
        print(f'[+] Log created with title "{title}"')
    except Exception as e:
        print(f"[-] Failed to create log: {e}")