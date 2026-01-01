from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import JobCreate, JobResponse, JobListResponse

from app.crud.job import create_job, list_jobs, update_job_status
from app.schemas import JobStatusUpdate



router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/jobs/add", response_model=JobResponse)
def add_job(data: JobCreate, db: Session = Depends(get_db)):
    return create_job(db, data.project_id, data.name)

@router.get("/jobs/list/{project_id}", response_model=JobListResponse)
def get_jobs(project_id: str, db: Session = Depends(get_db)):
    jobs = list_jobs(db, project_id)
    return {"jobs": jobs}


@router.post("/jobs/update_status", response_model=JobResponse)
def update_status(data: JobStatusUpdate, db: Session = Depends(get_db)):
    return update_job_status(db, data.job_id, data.status)
