import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

if not MONGODB_URL:
    raise ValueError("MONGODB_URL is not set in .env")

try:
    client = MongoClient(MONGODB_URL)

    # Test connection
    client.admin.command("ping")

    print("MongoDB connected successfully")

    # Database
    db = client["claimsense"]

    # Collections
    claims_collection = db["claims"]
    users_collection = db["users"]

except Exception as e:
    print("MongoDB connection failed")
    print(e)