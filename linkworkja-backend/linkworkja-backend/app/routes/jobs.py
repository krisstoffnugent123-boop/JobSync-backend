from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.job import JobCreate, JobResponse, JobFilter
from app.services.firebase_service import firebase_service
# from app.services.ai_service import ai_service
from app.routes.auth import verify_token

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/", response_model=JobResponse)
async def create_job(job: JobCreate, user_id: str = Depends(verify_token)):
    job_data = job.dict()
    
    # AI-enhance description if needed (disabled for now)
    # if len(job_data['description']) < 50:
    #     job_data['description'] = ai_service.generate_job_description(
    #         job_data['title'],
    #         job_data['parish'],
    #         job_data['required_skills']
    #     )
    
    job_id = firebase_service.create_job(job_data)
    job_data['id'] = job_id
    
    return JobResponse(**job_data)

@router.get("/", response_model=List[JobResponse])
async def get_jobs(
    parish: str = None,
    min_pay: float = None,
    max_pay: float = None
):
    filters = {}
    if parish:
        filters['parish'] = parish
    
    jobs = firebase_service.get_jobs(filters)
    
    # Apply pay filters in memory
    if min_pay:
        jobs = [j for j in jobs if j.get('pay', 0) >= min_pay]
    if max_pay:
        jobs = [j for j in jobs if j.get('pay', float('inf')) <= max_pay]
    
    return [JobResponse(**job) for job in jobs]

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    # Implementation for getting single job
    pass