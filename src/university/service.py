from src.database.collection import universities_collection        
from bson import ObjectId
from src.university.model import UniversityOut
from fastapi import HTTPException

async def read_university(university_id):
        university = await universities_collection.find_one({"_id": ObjectId(university_id)})
        if university:
            return UniversityOut(**university, id=str(university["_id"]))
        else:
            raise HTTPException(status_code=404, detail="University not found")
        
async def list_university(search_term,page_no,page_size):
    query = {}
    if search_term:
        # Case-insensitive search for universities containing the search term
        query["name"] = {"$regex": search_term, "$options": "i"}

    total_universities = await universities_collection.count_documents(query)

    skip_count = (page_no - 1) * page_size
    universities = await universities_collection.find(query).skip(skip_count).limit(page_size).to_list(length=None)
    
    universitiesId = [
        UniversityOut(**uni, id=str(uni["_id"])) for uni in universities
    ]
    return universitiesId
