# database.py
from motor.motor_asyncio import AsyncIOMotorClient
from utils.config import Config


client = AsyncIOMotorClient(Config.MONGO_URIs)
db = client["auth"]  
