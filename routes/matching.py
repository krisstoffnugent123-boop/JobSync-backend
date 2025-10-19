from fastapi import APIRouter, Depends
from typing import List
from models.matching import MatchScore, MatchRequest
from services.matching_service import matching_service
from routes.auth import verify_token

router = APIRouter(prefix="/matching", tags=["matching"])

@router.get("/recommendations", response_model=List[MatchScore])
async def get_recommendations(
    limit: int = 10,
    user_id: str = Depends(verify_token)
):
    recommendations = matching_service.get_recommendations(user_id, limit)
    return recommendations

@router.post("/score")
async def calculate_match_score(
    job_id: str,
    user_id: str = Depends(verify_token)
):
    """Calculate match score between user and specific job"""
    from services.firebase_service import firebase_service
    
    user = firebase_service.get_user(user_id)
    jobs = firebase_service.get_jobs({'id': job_id})
    
    if not jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    score = matching_service.calculate_match_score(user, jobs[0])
    return score