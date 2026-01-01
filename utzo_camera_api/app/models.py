from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String, unique=True, index=True)
    name = Column(String, unique=True, index=True)


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String, index=True)
    name = Column(String, index=True)
    status = Column(String, default="waiting")
    created_at = Column(DateTime, default=datetime.utcnow)


class Recording(Base):
    __tablename__ = "recordings"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(String, index=True)
    job_id = Column(Integer, nullable=True)
    file_path = Column(String)
    status = Column(String, default="in_progress")
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    type = Column(String, default="video")  # "video" or "snapshot"