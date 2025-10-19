from pydantic import BaseModel
from typing import List

class MatchScore(BaseModel):
    job_id: str
    score: float
    distance_km: float
    skill_match_percentage: float
    reasons: List[str] = []

class MatchRequest(BaseModel):
    user_id: str
    limit: int = 10