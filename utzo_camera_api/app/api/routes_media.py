from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Recording
import os

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/media/{media_id}")
def get_media(media_id: int, db: Session = Depends(get_db)):
    rec = db.query(Recording).filter(Recording.id == media_id).first()
    if not rec or not os.path.isfile(rec.file_path):
        raise HTTPException(status_code=404, detail="Media not found.")

    filename = os.path.basename(rec.file_path)
    return FileResponse(path=rec.file_path, filename=filename, media_type="application/octet-stream")
