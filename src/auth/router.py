from fastapi import APIRouter, HTTPException,Depends
from src.auth.model import User ,LoginInput,ResetPassWordInput,ForgotPasswordInput,ResetPasswordOtpInput,UpdateProfileInput
from src.auth.helper import get_current_user
from src.auth import service

router = APIRouter()



@router.post("/signup/",tags=["Auth"])
async def register_user(user: User):
    """
    api is for  user registration 
    """
    return await service.signup(user)

@router.post("/login/",tags=["Auth"])
async def login_user(user: LoginInput):
    """
    api is for  user login 
    """
    return await service.login(user)

@router.post("/reset-password/",tags=["Auth"])
async def change_password(reset_password_input:ResetPassWordInput,current_user: str = Depends(get_current_user)):
    """
    api is for change password
    """
    return await service.reset_password(reset_password_input,current_user)

@router.post("/forgot-password/",tags=["Forgot Password"])
async def forgot_password(forgot_password_input: ForgotPasswordInput):
    """
    api is for forgot password
    """
    return await service.forgot_password(forgot_password_input.__dict__["email"])

@router.post("/verify-otp/",tags=["Forgot Password"])
async def verify_otp(request):
    return await service.verify_otp(request)

@router.put("/reset-password-after-otp/",tags=["Forgot Password"])
async def reset_password_after_otp(reset_password_after_otp : ResetPasswordOtpInput):
    return await service.reset_password_after_otp(reset_password_after_otp.__dict__["email"],reset_password_after_otp.__dict__["new_password"])

@router.put("/update-profile/",tags=["User"])
async def update_profile(update_profile : UpdateProfileInput,current_user: str = Depends(get_current_user)):
    """
    user can update their name and phone number
    """
    return await service.update_profile(update_profile,current_user)

@router.get("/profile/",tags=["User"])
async def profile(current_user: str = Depends(get_current_user)):
    """
    to get user' info  by passing token in header of request 
    info  include name ,phone number ,email
    """
    return await service.profile(current_user)