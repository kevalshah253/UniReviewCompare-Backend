from typing_extensions import Annotated, Doc
from fastapi import HTTPException, Depends, Request, Security
from fastapi.security.http import HTTPAuthorizationCredentials
from passlib.context import CryptContext
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta
from src.utils.config import Config
from starlette import status
import jwt
from typing import Optional
from src.database.collection import user_collection
from bson import ObjectId

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM
    )
    return encoded_jwt


def decode_jwt(token):
    jwt_token = token
    if jwt_token:
        try:
            decoded_token = jwt.decode(jwt_token, Config, algorithms=["HS256"])
            return decoded_token
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token is invalied")
    else:
        raise HTTPException(status_code=401, detail="Token is missing")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    if credentials:
        token = credentials.credentials
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            user_id: str = payload.get("sub")
            id_obj = ObjectId(user_id)
            user = await user_collection.find_one({"_id": id_obj})
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication credentials",
                )
            return user
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token or expired token",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )
