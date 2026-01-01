from sqlalchemy.orm import Session
from app.models import Project, Job
from datetime import datetime
import os

def create_project(db: Session, project_id: str, name: str):
    existing = db.query(Project).filter(
        (Project.project_id == project_id) | (Project.name == name)
    ).first()
    if existing:
        return {"message": "Project with same ID or Name already exists."}

    new_project = Project(project_id=project_id, name=name)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    # Create project folder
    safe_project = f"{project_id}_{name}".replace(" ", "_")
    project_dir = os.path.join("recordings", safe_project)
    os.makedirs(project_dir, exist_ok=True)

    # Create default job under this project
    default_job = Job(
        project_id=project_id,
        name="default",
        status="waiting",
        created_at=datetime.utcnow()
    )
    db.add(default_job)
    db.commit()

    # Create default job folder
    job_dir = os.path.join(project_dir, "default")
    os.makedirs(job_dir, exist_ok=True)

    return {"message": "Project created successfully with default job."}
