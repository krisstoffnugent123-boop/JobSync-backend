from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.gig import GigCreate, GigResponse, GigCompletion
from app.services.firebase_service import firebase_service
from app.services.ai_service import ai_service
from app.routes.auth import verify_token

router = APIRouter(prefix="/gigs", tags=["gigs"])

@router.post("/", response_model=GigResponse)
async def create_gig(gig: GigCreate, user_id: str = Depends(verify_token)):
    gig_data = gig.dict()
    gig_id = firebase_service.create_gig(gig_data)
    gig_data['id'] = gig_id
    return GigResponse(**gig_data)

@router.get("/available", response_model=List[GigResponse])
async def get_available_gigs(parish: str = None):
    gigs = firebase_service.get_available_gigs(parish)
    return [GigResponse(**gig) for gig in gigs]

@router.post("/{gig_id}/claim")
async def claim_gig(gig_id: str, user_id: str = Depends(verify_token)):
    success = firebase_service.claim_gig(gig_id, user_id)
    if not success:
        raise HTTPException(status_code=400, detail="Unable to claim gig")
    return {"message": "Gig claimed successfully"}

@router.post("/complete")
async def complete_gig(completion: GigCompletion, user_id: str = Depends(verify_token)):
    success = firebase_service.complete_gig(completion.gig_id, user_id)
    if not success:
        raise HTTPException(status_code=400, detail="Unable to complete gig")
    return {"message": "Gig completed successfully", "payment_processed": True}

@router.post("/generate-batch")
async def generate_gigs(count: int = 5, user_id: str = Depends(verify_token)):
    """AI-generate multiple micro-gigs"""
    gigs = ai_service.generate_micro_gigs(count)
    created_gigs = []
    
    for gig in gigs:
        gig['agency_id'] = user_id
        gig_id = firebase_service.create_gig(gig)
        gig['id'] = gig_id
        created_gigs.append(gig)
    
    return {"generated": len(created_gigs), "gigs": created_gigs}