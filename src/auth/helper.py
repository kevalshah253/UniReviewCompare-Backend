from passlib.context import CryptContext
from datetime import datetime, timedelta
from utils.config import Constant
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Constant.SECRET_KEY, algorithm=Constant.ALGORITHM)
    return encoded_jwt
