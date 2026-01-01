import os, json

CONFIG_PATH = "config/storage_path.json"
DEFAULT_MEDIA_ROOT = "recordings"

def get_storage_path():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
            return data.get("media_root", DEFAULT_MEDIA_ROOT)
    return DEFAULT_MEDIA_ROOT

def set_storage_path(path: str):
    os.makedirs("config", exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump({"media_root": path}, f)
    return True

def list_usb_mounts():
    mounts = []
    with open("/proc/mounts", "r") as f:
        for line in f:
            parts = line.split()
            if "/dev/sd" in parts[0] and parts[1].startswith("/media"):
                mounts.append(parts[1])
    return mounts
