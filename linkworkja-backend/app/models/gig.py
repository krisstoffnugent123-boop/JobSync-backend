from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class GigBase(BaseModel):
    title: str
    description: str
    parish: str
    payment: float
    estimated_time: str  # e.g., "2 hours"
    difficulty: str  # easy, medium, hard

class GigCreate(GigBase):
    agency_id: str

class GigResponse(GigBase):
    id: str
    agency_id: str
    created_at: datetime
    status: str = "available"  # available, claimed, completed
    claimed_by: Optional[str] = None
    completed_at: Optional[datetime] = None

class GigCompletion(BaseModel):
    gig_id: str
    user_id: str
    completion_proof: Optional[str] = None