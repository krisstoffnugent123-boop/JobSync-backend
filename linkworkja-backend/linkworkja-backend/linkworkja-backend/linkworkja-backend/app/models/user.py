from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    JOB_SEEKER = "job_seeker"
    BUSINESS = "business"
    GOVERNMENT = "government"

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    parish: str
    role: UserRole

class UserCreate(UserBase):
    password: str
    skills: Optional[List[str]] = []

class UserResponse(UserBase):
    id: str
    skills: List[str] = []
    created_at: datetime
    completed_gigs: int = 0
    total_earnings: float = 0.0

class UserInDB(UserResponse):
    hashed_password: str