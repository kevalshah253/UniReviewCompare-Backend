from fastapi import APIRouter, HTTPException, Request, Depends
from src.university.model import University, UniversityFilters, UniversityOut, UniComment
from src.university import service
from typing import List
from src.database.collection import universities_collection
from src.auth.helper import get_current_user


router = APIRouter()


PAGE_SIZE = 8


@router.get("/university/{university_id}", tags=["Universiry"])
async def university(university_id: str):
    """
    api is for  user registration 
    """
    return await service.read_university(university_id)


# Get Universities API
@router.get("/universities/", tags=["Universiry"])
async def get_universities(
    page_no: int = 1,
    page_size: int = PAGE_SIZE,
    search_term: str = None
):
    return await service.list_university(search_term, page_no, page_size)


@router.post("/university/upsert_review")
async def add_review(uni_comment: UniComment, current_user: str = Depends(get_current_user)):
    """
    per university only one comment allowed per user

    upsert meaning 

    for create and update use the same api
    """
    return await service.add_review(current_user, uni_comment.__dict__['university_id'], uni_comment.__dict__['comment'], uni_comment.__dict__['star'])
