from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import (
    RecordingStartRequest, RecordingStopRequest, RecordingResponse, SnapshotRequest
)
from app.models import Recording
from app.crud.recording import start_recording, stop_recording, take_snapshot
from datetime import datetime
from app.schemas import MediaListResponse
from app.crud.recording import get_media_by_job

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/record/start", response_model=RecordingResponse)
def start_rec(req: RecordingStartRequest, db: Session = Depends(get_db)):
    existing = db.query(Recording).filter(Recording.status == "in_progress").first()
    if existing:
        return {"message": "Recording already in progress."}
    path = start_recording(db, req.project_id, req.job_id, req.rtsp_url)
    if not path:
        return {"message": "Recording failed to start."}
    rec = Recording(
    project_id=req.project_id,
    job_id=req.job_id,   # 👈 required
    file_path=path,
    status="in_progress",
    type="video",
    start_time=datetime.utcnow()
    )
    db.add(rec)
    db.commit()
    return {"message": f"Recording started: {path}"}

@router.post("/record/stop", response_model=RecordingResponse)
def stop_rec(req: RecordingStopRequest, db: Session = Depends(get_db)):
    path, project_id = stop_recording()
    if not path:
        return {"message": "No recording is in progress."}
    rec = db.query(Recording).filter(
        Recording.project_id == project_id,
        Recording.file_path == path,
        Recording.status == "in_progress"
    ).first()
    if rec:
        rec.status = "complete"
        rec.end_time = datetime.utcnow()
        db.commit()
    return {"message": f"Recording stopped: {path}"}

@router.post("/record/snapshot", response_model=RecordingResponse)
def snapshot(req: SnapshotRequest, db: Session = Depends(get_db)):
    path = take_snapshot(db, req.project_id, req.job_id, req.rtsp_url)
    if not path:
        return {"message": "Snapshot failed."}
    rec = Recording(
    project_id=req.project_id,
    job_id=req.job_id,   
    file_path=path,
    status="complete",
    type="snapshot",
    start_time=datetime.utcnow(),
    end_time=datetime.utcnow()
    )
    db.add(rec)
    db.commit()
    return {"message": f"Snapshot saved: {path}"}


@router.get("/record/media/{job_id}", response_model=MediaListResponse)
def media_by_job(job_id: int, db: Session = Depends(get_db)):
    results = get_media_by_job(db, job_id)
    return {"media": results}
