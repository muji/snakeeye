from sqlalchemy.orm import Session
from app.models import Job
from datetime import datetime
import os

def create_job(db: Session, project_id: str, name: str):
    existing = db.query(Job).filter(Job.project_id == project_id, Job.name == name).first()
    if existing:
        return {"message": "Job with same name already exists for this project."}

    new_job = Job(project_id=project_id, name=name, status="waiting", created_at=datetime.utcnow())
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    # Create recording folder path
    safe_project = project_id.replace(" ", "_")
    safe_job = name.replace(" ", "_")
    folder = os.path.join("recordings", safe_project, safe_job)
    os.makedirs(folder, exist_ok=True)

    return {"message": "Job created successfully.", "job_id": new_job.id}

def list_jobs(db: Session, project_id: str):
    return db.query(Job).filter(Job.project_id == project_id).all()

def update_job_status(db: Session, job_id: int, status: str):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return {"message": "Job not found."}
    
    job.status = status
    db.commit()
    return {"message": f"Job status updated to {status}."}
