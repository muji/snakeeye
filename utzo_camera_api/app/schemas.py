from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List

class ProjectCreate(BaseModel):
    project_id: str
    name: str

class ProjectResponse(BaseModel):
    message: str



class JobCreate(BaseModel):
    project_id: str
    name: str

class JobOut(BaseModel):
    id: int
    project_id: str
    name: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

class JobResponse(BaseModel):
    message: str
    job_id: Optional[int] = None

class JobListResponse(BaseModel):
    jobs: List[JobOut]

class JobStatusUpdate(BaseModel):
    job_id: int
    status: str  # expected values: "waiting", "in_progress", "finished"

class RecordingStartRequest(BaseModel):
    project_id: str
    job_id: int  
    rtsp_url: str


class RecordingStopRequest(BaseModel):
    project_id: str

class RecordingResponse(BaseModel):
    message: str

class SnapshotRequest(BaseModel):
    project_id: str
    rtsp_url: str
    
class WiFiConfig(BaseModel):
    interface: str
    ssid: str
    password: str
    use_dhcp: bool = True
    static_ip: Optional[str] = None
    gateway: Optional[str] = None
    dns: Optional[str] = None

class EthernetConfig(BaseModel):
    interface: str
    use_dhcp: bool = True
    static_ip: Optional[str] = None
    gateway: Optional[str] = None
    dns: Optional[str] = None

class InterfaceStatus(BaseModel):
    interface: str
    ip: Optional[str]
    mac: Optional[str]
    connected: bool
    ssid: Optional[str] = None
    signal_strength: Optional[int] = None    

class MediaOut(BaseModel):
    id: int
    job_id: Optional[int]
    project_id: str
    file_path: str
    type: str
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    status: str

    class Config:
        orm_mode = True

class MediaListResponse(BaseModel):
    media: List[MediaOut]


class AudioStartRequest(BaseModel):
    project_id: str
    job_id: int

class AudioStopRequest(BaseModel):
    project_id: str
    job_id: int

