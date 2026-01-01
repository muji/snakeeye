from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import AudioStartRequest, AudioStopRequest, RecordingResponse
from app.database import SessionLocal
from app.models import Recording
from app.crud.recording import start_audio_recording, stop_audio_recording
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/audio/start", response_model=RecordingResponse)
def start_audio(req: AudioStartRequest, db: Session = Depends(get_db)):
    path = start_audio_recording(db, req.project_id, req.job_id)
    if not path:
        return {"message": "Audio recording already in progress or failed to start."}
    rec = Recording(
        project_id=req.project_id,
        job_id=req.job_id,
        file_path=path,
        status="in_progress",
        type="audio",
        start_time=datetime.utcnow()
    )
    db.add(rec)
    db.commit()
    return {"message": f"Audio recording started: {path}"}

@router.post("/audio/stop", response_model=RecordingResponse)
def stop_audio(req: AudioStopRequest, db: Session = Depends(get_db)):
    path, project_id, job_id = stop_audio_recording()
    if not path:
        return {"message": "No audio recording in progress."}
    rec = db.query(Recording).filter(
        Recording.project_id == project_id,
        Recording.job_id == job_id,
        Recording.file_path == path,
        Recording.status == "in_progress",
        Recording.type == "audio"
    ).first()
    if rec:
        rec.status = "complete"
        rec.end_time = datetime.utcnow()
        db.commit()
    return {"message": f"Audio recording stopped: {path}"}
