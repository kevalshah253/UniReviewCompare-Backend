# database.py
from motor.motor_asyncio import AsyncIOMotorClient
from utils.config import Config


client = AsyncIOMotorClient(Config.MONGO_URI)
db = client["auth"]
user_collection = db["users"]
