from pydantic import BaseModel,HttpUrl
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
    uniReview: str = None

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