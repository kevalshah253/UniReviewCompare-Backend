from pydantic import BaseModel, EmailStr, constr, validator


class User(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=50)
    is_admin: bool = False

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
    password: constr(min_length=8, max_length=50)