from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["loan_agent"]

conversations = db["conversations"]
user_data = db["user_data"]
transactions = db["transactions"]   # logs / audit
