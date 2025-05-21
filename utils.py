import os
import string
import random
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv("config.env")

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
files_col = db["files"]
torrents_col = db["torrents"]

def generate_hash(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def save_file_record(user_id, hash_id, chat_id, message_id, file_name):
    files_col.insert_one({
        "user_id": user_id,
        "hash": hash_id,
        "chat_id": chat_id,
        "message_id": message_id,
        "file_name": file_name
    })

def get_file_record(hash_id):
    return files_col.find_one({"hash": hash_id})

def get_last_file_by_user(user_id):
    return files_col.find_one({"user_id": user_id}, sort=[("_id", -1)])

def save_torrent_record(user_id, hash_id, info):
    torrents_col.insert_one({
        "user_id": user_id,
        "hash": hash_id,
        **info
    })

def get_torrent_record(hash_id):
    return torrents_col.find_one({"hash": hash_id})
