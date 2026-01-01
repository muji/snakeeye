from fastapi import FastAPI
from app.api.routes_project import router as project_router
from app.database import Base, engine
from app.api.routes_recording import router as recording_router
from app.api.routes_job import router as job_router
from app.api.routes_audio import router as audio_router
from app.api.routes_media import router as media_router
from app.api.routes_system import router as system_router







app = FastAPI(title="UTZO Camera API")
Base.metadata.create_all(bind=engine)
app.include_router(project_router, prefix="/api")
app.include_router(job_router, prefix="/api")
app.include_router(audio_router, prefix="/api")
app.include_router(media_router, prefix="/api")
app.include_router(system_router, prefix="/api")
