from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional

class User(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=50) # type: ignore
    is_admin: bool = False
    name: str
    is_verified: bool = False
    is_deleted: bool = False
    is_admin: bool = False
    phone: Optional[constr(min_length=10, max_length=13)] # type: ignore

    @validator("password")
    def validate_password(cls, v):
        # Check if password contains at least one uppercase letter, one lowercase letter, and one digit
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        return v


class LoginInput(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=50) # type: ignore

class ResetPassWordInput(BaseModel):
    new_password:constr(min_length=8, max_length=50) # type: ignore
    old_password:constr(min_length=8, max_length=50) # type: ignore

class ForgotPasswordInput(BaseModel):
    email: EmailStr

class VerifyOtpInput(BaseModel):
    email: EmailStr
    otp: str

class ResetPasswordOtpInput(BaseModel):
    email: EmailStr
    new_password:constr(min_length=8, max_length=50) # type: ignore

class UpdateProfileInput(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "phone_number": "123-456-7890",
                "email": "test@test.com"
            }
        }
