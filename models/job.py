from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class JobBase(BaseModel):
    title: str
    description: str
    parish: str
    pay: float
    required_skills: List[str] = []
    job_type: str  # full-time, part-time, contract

class JobCreate(JobBase):
    employer_id: str

class JobResponse(JobBase):
    id: str
    employer_id: str
    created_at: datetime
    status: str = "active"  # active, filled, expired
    applications_count: int = 0

class JobFilter(BaseModel):
    parish: Optional[str] = None
    min_pay: Optional[float] = None
    max_pay: Optional[float] = None
    skills: Optional[List[str]] = None
    job_type: Optional[str] = None