from fastapi import  APIRouter, HTTPException


router = APIRouter(tags=['auth'])

@router.get("/")    
async def root():
    return {"Status":"ok"}