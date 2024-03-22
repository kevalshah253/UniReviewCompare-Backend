from src.database.collection import universities_collection
from src.utils.redis import redis_uri
from bson import ObjectId
from src.university.model import UniversityOut
from fastapi import HTTPException
from datetime import datetime
import json


def flush_keys_with_prefix(redis_client, prefix):
    keys = redis_client.keys(f"{prefix}*")
    if keys:
        redis_client.delete(*keys)
        print(f"Deleted {len(keys)} keys with prefix '{prefix}'")
    else:
        print(f"No keys found with prefix '{prefix}'")


async def get_uni_by_id(id, cache_key):
    university = await universities_collection.aggregate([
        {"$match": {"_id": ObjectId(id)}},  # Match the document by its ID
        {
            "$addFields": {
                # Calculate the average review stars for the document
                "uniReview": {"$avg": "$reviews.stars"}
            }
        }
    ]).next()

    if university:
        university["_id"] = str(university["_id"])
        # If there are no reviews for the university, set the average review to 0
        university["uniReview"] = university.get("uniReview", 0)
        serialized_result = json.dumps(university, default=str)
        redis_uri.set(cache_key, serialized_result, ex=360000)
        return university
    return None


async def read_university(university_id):
    cache_key = f"university:{university_id}"

    # Check if result is cached
    cached_result = redis_uri.get(cache_key)
    if cached_result:
        print(f"redis cached with key {cache_key} hit")
        return json.loads(cached_result)

    university = await get_uni_by_id(university_id, cache_key)
    if not university:
        raise HTTPException(status_code=404, detail="University not found")

    return university


async def list_university(search_term, page_no, page_size):

    cache_key = f"list_university:{search_term}:{page_no}:{page_size}"

    # Check if result is cached
    cached_result = redis_uri.get(cache_key)
    if cached_result:
        print(f"redis cached with key {cache_key} hit")
        return json.loads(cached_result)

    query = {}
    if search_term:
        # Case-insensitive search for universities containing the search term
        query["name"] = {"$regex": search_term, "$options": "i"}

    pipeline = [
        {"$match": query},  # Match documents based on the search criteria
        {
            "$addFields": {
                # Calculate the average review stars for each document
                "uniReview": {"$avg": "$reviews.stars"}
            }
        },
        # Skip documents based on pagination
        {"$skip": (page_no - 1) * page_size},
        {"$limit": page_size}  # Limit the number of documents per page
    ]

    universities = await universities_collection.aggregate(pipeline).to_list(None)

    # Iterate through each university document
    for uni in universities:
        # Convert ObjectId to string for consistency
        uni["_id"] = str(uni["_id"])
        # If there are no reviews for the university, set the average review to 0
        uni["uniReview"] = uni.get("uniReview", 0)

    serialized_result = json.dumps(universities, default=str)
    redis_uri.set(cache_key, serialized_result, ex=360000)

    return universities


async def add_review(current_user, university_id, review, star):
    cache_key = f"university:{university_id}"
    try:
        uni = await universities_collection.find_one({"_id": ObjectId(university_id)})
        reviews = uni.get("reviews")
        if reviews:
            for rev in reviews:
                if rev.get("user_id") == str(current_user["_id"]):
                    # Update the existing review
                    result = await universities_collection.update_one(
                        {"_id": ObjectId(university_id), "reviews.user_id": str(
                            current_user["_id"])},
                        {"$set": {"reviews.$.review": review,
                                  "reviews.$.stars": star,
                                  "reviews.$.updated_at": datetime.utcnow()}}
                    )
                    if result.modified_count == 1:
                        university = await get_uni_by_id(university_id, cache_key)
                        flush_keys_with_prefix(redis_uri, 'list_university:')
                        return {"message": "Review updated successfully", "status": 200, 'data': university}
                    else:
                        raise HTTPException(
                            status_code=500, detail="Failed to update review")
        if university_id is None or review is None:
            return {"message": "University id and review are required", "status": 400}
        else:
            university = await universities_collection.find_one({"_id": ObjectId(university_id)})
            if university:
                result = await universities_collection.update_one(
                    {"_id": ObjectId(university_id)},
                    {
                        "$push": {
                            "reviews": {
                                "review": review,
                                "stars": star,
                                "user_id": str(current_user["_id"]),
                                "created_at": datetime.utcnow(),
                                "updated_at": datetime.utcnow()
                            }
                        }
                    }
                )
                if result.modified_count == 1:
                    university = await get_uni_by_id(university_id, cache_key)
                    flush_keys_with_prefix(redis_uri, 'list_university:')
                    return {"message": "Review added successfully", "status": 200, 'data': university}
                else:
                    raise HTTPException(
                        status_code=500, detail="Failed to add review")
            else:
                raise HTTPException(
                    status_code=404, detail="University not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
