import subprocess
import os
from datetime import datetime

from requests import Session

from app.models import Recording

import signal

audio_process = None
current_audio = {}


recording_process = None
current_recording = {}


from app.models import Project, Job
from app.crud.system import get_storage_path

def resolve_media_folder(db: Session, project_id: str, job_id: int) -> str:
    project = db.query(Project).filter(Project.project_id == project_id).first()
    job = db.query(Job).filter(Job.id == job_id).first()
    if not project or not job:
        return None

    safe_project = f"{project_id}_{project.name}".replace(" ", "_")
    safe_job = job.name.replace(" ", "_")
    base_path = get_storage_path()  # from JSON config

    folder = os.path.join(base_path, safe_project, safe_job)
    os.makedirs(folder, exist_ok=True)
    return folder


def start_recording(db: Session, project_id: str, job_id: int, rtsp_url: str) -> str:

    global recording_process, current_recording
    if recording_process:
        return None

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{project_id}_{now}.mp4"
    folder = resolve_media_folder(db, project_id, job_id)
    os.makedirs(folder, exist_ok=True)
    full_path = os.path.join(folder, filename)

    cmd = [
        "gst-launch-1.0", "rtspsrc", f"location={rtsp_url}", "!", 
        "rtph264depay", "!", "h264parse", "!", "mp4mux", "!", 
        "filesink", f"location={full_path}"
    ]

    recording_process = subprocess.Popen(cmd)
    current_recording = {"project_id": project_id, "file_path": full_path}
    return full_path

def stop_recording():
    global recording_process, current_recording
    if recording_process:
        recording_process.terminate()
        recording_process.wait()
        path = current_recording["file_path"]
        project_id = current_recording["project_id"]
        recording_process = None
        current_recording = {}
        return path, project_id
    return None, None

def take_snapshot(db: Session, project_id: str, job_id: int, rtsp_url: str) -> str:

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{project_id}_{now}.jpg"
    folder = resolve_media_folder(db, project_id, job_id)
    os.makedirs(folder, exist_ok=True)
    full_path = os.path.join(folder, filename)

    cmd = [
        "gst-launch-1.0", "-e",
        "rtspsrc", f"location={rtsp_url}", "num-buffers=1", "!", 
        "decodebin", "!", 
        "videoconvert", "!", 
        "jpegenc", "!", 
        "filesink", f"location={full_path}"
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        return full_path
    return None


def get_media_by_job(db: Session, job_id: int):
    return db.query(Recording).filter(Recording.job_id == job_id).all()



def start_audio_recording(db: Session, project_id: str, job_id: int) -> str:
    global audio_process, current_audio
    if audio_process:
        return None

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"audio_{now}.wav"
    folder = resolve_media_folder(db, project_id, job_id)

    os.makedirs(folder, exist_ok=True)
    full_path = os.path.join(folder, filename)

    cmd = [
        "arecord", "-D", "plughw:1,0", "-f", "cd", "-t", "wav", "-q", full_path
    ]

    audio_process = subprocess.Popen(cmd)
    current_audio = {"project_id": project_id, "job_id": job_id, "file_path": full_path}
    return full_path

def stop_audio_recording():
    global audio_process, current_audio
    if audio_process:
        audio_process.send_signal(signal.SIGINT)
        audio_process.wait()
        path = current_audio["file_path"]
        project_id = current_audio["project_id"]
        job_id = current_audio["job_id"]
        audio_process = None
        current_audio = {}
        return path, project_id, job_id
    return None, None, None
