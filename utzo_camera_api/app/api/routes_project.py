import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import ProjectCreate, ProjectResponse
from app.crud.project import create_project

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/projects/add", response_model=ProjectResponse)
def add_project(data: ProjectCreate, db: Session = Depends(get_db)):
    return create_project(db, data.project_id, data.name)
