from fastapi import APIRouter, HTTPException
from auth.model import User ,LoginInput
from auth import service

router = APIRouter(tags=["auth"])


@router.post("/signup/")
async def register_user(user: User):
    return await service.signup(user)


@router.post("/login/")
async def login_user(user: LoginInput):
    return await service.login(user)
