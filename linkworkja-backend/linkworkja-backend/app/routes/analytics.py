from fastapi import APIRouter, Depends
from app.services.firebase_service import firebase_service
from app.services.ai_service import ai_service
from app.routes.auth import verify_token

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/dashboard")
async def get_dashboard_analytics(user_id: str = Depends(verify_token)):
    data = firebase_service.get_analytics_data()
    insights = ai_service.generate_analytics_insights(data)
    
    return {
        "metrics": data,
        "ai_insights": insights
    }

@router.get("/parish-stats")
async def get_parish_statistics():
    data = firebase_service.get_analytics_data()
    return data['gigs_by_parish']