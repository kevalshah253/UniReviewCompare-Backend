from pydantic import BaseModel, HttpUrl, Field, validator
from typing import List
from enum import Enum


class University(BaseModel):
    name: str
    location: str
    established_year: int
    total_students: int = None
    courses_offered: List[str] = []
    tuition_fee: float = None
    acceptance_rate: float = None
    student_faculty_ratio: float = None
    campus_size: float = None
    website: str = None
    ranking: int = None
    image_url: str = None
    google_review: float = None
    uniReview: float = None
    reviews: List[dict] = []


class UniversityFilters(BaseModel):
    country: str = None
    ranking: int = None


class FilterType(str, Enum):
    country = "country"
    ranking = "ranking"


class UniversityOut(University):
    id: str


class UniversityIn(University):
    pass


class UniComment(BaseModel):
    university_id: str
    comment: str
    star: float = Field(..., ge=0, le=5,
                        description="Rating between 0 and 5, inclusive")

    class Config:
        schema_extra = {
            "example": {
                "university_id": "user123",
                "comment": "This is a great university!",
                "star": 4.75
            }
        }

    @validator("star", pre=True, always=True)
    def round_star(cls, v):
        return round(v, 2)
