import os
import secrets
from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGO_URI = os.getenv("MONGODB_URI")
    ACCESS_TOKEN_EXPIRE_HOURS= os.getenv("ACCESS_TOKEN_EXPIRE_HOURS")
    SECRET_KEY=os.getenv("SECRET_KEY")
    ALGORITHM=os.getenv("ALGORITHM")