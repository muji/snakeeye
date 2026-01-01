from fastapi import APIRouter
import os

from app.crud.system import list_usb_mounts, set_storage_path, get_storage_path
from fastapi import Body

router = APIRouter()

@router.get("/system/temperature")
def read_pi_temperature():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_millic = int(f.read().strip())
            temp_c = temp_millic / 1000.0
            return {"temperature_celsius": round(temp_c, 2)}
    except Exception as e:
        return {"error": f"Failed to read temperature: {str(e)}"}



@router.get("/system/storage/usb")
def list_usb_storage():
    return {"mounts": list_usb_mounts()}

@router.post("/system/storage/set")
def set_path(path: str = Body(..., embed=True)):
    success = set_storage_path(path)
    return {"message": "Storage path set successfully." if success else "Failed to set path."}

@router.get("/system/storage/current")
def get_path():
    return {"media_root": get_storage_path()}
