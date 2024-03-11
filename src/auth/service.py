from src.database.collection import user_collection
from fastapi import HTTPException
from src.auth.helper import pwd_context, create_access_token,decode_jwt
from src.auth.utils import send_otp,generate_otp
from src.utils.config import Config
from bson import ObjectId
from datetime import datetime, timedelta

async def find_user(user):
    existing_user = await user_collection.find_one({"email": user.email})
    return existing_user


async def signup(user):
    existing_user = await find_user(user)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    user_data = {
        "email": user.email,
        "password": hashed_password,
        "name": user.name,
        "phone":user.phone,
        "isVerified": False,
        "createdAt":datetime.utcnow(),'updatedAt':datetime.utcnow(),
        "is_deleted":False,'is_admin':False
                }
    result = await user_collection.insert_one(user_data)
    return {"id": str(result.inserted_id), "email": user.email}


async def login(user):
    existing_user = await find_user(user)
    if not existing_user or not pwd_context.verify(
        user.password, existing_user["password"]
    ):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token_expires = timedelta(hours=Config.ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"sub": str(existing_user["_id"])}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

async def reset_password(input,user):
    new_password = input.__dict__["new_password"]
    old_password = input.__dict__["old_password"]
    if not pwd_context.verify(old_password, user['password']):
        raise HTTPException(status_code=400, detail="Invalid old password")    
    hashed_new_password = pwd_context.hash(new_password)
    if new_password == old_password:
        raise HTTPException(status_code=400, detail="New password is same as old password")
    id_obj = ObjectId(user["_id"])
    passw = await user_collection.update_one({"_id": id_obj}, {"$set": {"password": hashed_new_password}})
    if passw:
        return {"message": "Password reset successful"}
    else:
        return {"message": "Password reset not successful"}
    

async def forgot_password(email):
    existing_user = await user_collection.find_one({"email": email})
    if not existing_user:
        raise HTTPException(status_code=400, detail="Email not registered")

    # Generate and save OTP
    otp = generate_otp()
    await user_collection.update_one({"email": email}, {"$set": {"otp": otp}})

    send_otp(email, otp)

    return {"message": "OTP sent to your email"}

async def verify_otp(email, otp):
    user = await user_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=400, detail="Email not registered")

    stored_otp = user.get("otp")
    if not stored_otp or stored_otp != otp:
        raise HTTPException(status_code=401, detail="Invalid OTP")

    return {"message": "OTP verified successfully"}

async def reset_password_after_otp(email,new_password):
    user = await user_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=400, detail="Email not registered")

    hashed_new_password = pwd_context.hash(new_password)
    await user_collection.update_one({"email": email}, {"$set": {"password": hashed_new_password, "otp": None}})

    return {"message": "Password reset successful"} 


async def update_profile(new_email,new_phone,new_name,user):
    update_query = {}
    update_message = "Profile not updated"
    if new_email:
        if new_email != user.get("email"):
            existing_user_with_email = await user_collection.find_one({"email": new_email})
            if existing_user_with_email:
                raise HTTPException(status_code=400, detail="Email already registered")
            else:
                update_query["email"] = new_email
                update_message = "Profile updated successfully"

    if new_phone:
        if new_phone != user.get("phone"):
            existing_user_with_phone = await user_collection.find_one({"phone": new_phone})
            if existing_user_with_phone:
                raise HTTPException(status_code=400, detail="Phone number already registered")
            else:
                update_query["phone"] = new_phone
                update_message = "Profile updated successfully"

    if new_name:
        if new_name != user.get("name"):
            update_query["name"] = new_name
            update_message = "Profile updated successfully"

    if update_query:
        await user_collection.update_one({"_id": ObjectId(user['_id'])}, {"$set": update_query})
    return {"message": update_message}


async def profile(user): 
    user = await user_collection.find_one({"_id": user["_id"]})    
    if user:
        return {"email":user['email'],"name":user['name'],"phone":user['phone']} 
    else:
        return {"message": "User not found"}