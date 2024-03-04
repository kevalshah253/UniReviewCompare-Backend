from database.collection import user_collection
from fastapi import HTTPException
from auth.helper import pwd_context, create_access_token
from utils.config import Constant
from datetime import datetime, timedelta

async def find_user(user):
    existing_user = await user_collection.find_one({"email": user.email})
    return existing_user


async def signup(user):
    existing_user = await find_user(user)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    user_data = {"email": user.email, "password": hashed_password}
    result = await user_collection.insert_one(user_data)
    return {"id": str(result.inserted_id), "email": user.email}


async def login(user):
    existing_user = await find_user(user)
    if not existing_user or not pwd_context.verify(
        user.password, existing_user["password"]
    ):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token_expires = timedelta(hours=Constant.ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"sub": str(existing_user["_id"])}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
