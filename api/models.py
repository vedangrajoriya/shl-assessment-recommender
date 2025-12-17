from pydantic import BaseModel
from typing import List

class Assessment(BaseModel):
    url: str
    name: str
    adaptive_support: str   # "Yes" / "No"
    description: str
    duration: int
    remote_support: str     # "Yes" / "No"
    test_type: List[str]

class RecommendResponse(BaseModel):
    recommended_assessments: List[Assessment]
