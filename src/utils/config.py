import os
import secrets
from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGO_URI = os.getenv("MONGODB_URI")


class Constant:
    ACCESS_TOKEN_EXPIRE_HOURS = 24
    SECRET_KEY = "fastAPI"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS = 48
