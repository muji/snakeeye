
from fastapi import APIRouter
from app.schemas import WiFiConfig, EthernetConfig
from app.crud import network

router = APIRouter()

@router.get("/network/interfaces")
def get_interfaces():
    return network.list_interfaces()

@router.post("/network/configure_wifi")
def configure_wifi(data: WiFiConfig):
    result = network.configure_wifi(data)
    return {"message": "WiFi configured" if result else "Failed"}

@router.post("/network/configure_ethernet")
def configure_ethernet(data: EthernetConfig):
    result = network.configure_ethernet(data)
    return {"message": "Ethernet configured" if result else "Failed"}

@router.get("/network/status")
def interface_status(interface: str):
    return network.get_interface_status(interface)
