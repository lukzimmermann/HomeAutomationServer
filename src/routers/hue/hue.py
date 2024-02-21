from fastapi import APIRouter
from pydantic import BaseModel

from src.routers.hue.hue_service import HueService

class Dimm(BaseModel):
    light_id: str
    duration: int
    brightness: int

hue_service = HueService()

router = APIRouter(prefix="/hue", tags=["Hue Lights"])

@router.get("/getLights/", tags=["Hue Lights"])
async def getLights():
    return hue_service.get_rooms_from_hue()

def print_something():
    print('Dini Mueter')

@router.put("/setRoom/{room_id}")
async def setRoom(room_id):
    return hue_service.set_room(room_id)

@router.get("/cinema/")
async def setRoom():
    return hue_service.cinema_mode()

@router.put("/dimm_light")
async def dimm_light(data: Dimm):
    return hue_service.dimm_light(data.light_id, data.duration, data.brightness)

@router.get("/get_automation_state/{automation_id}")
async def get_automation_state(automation_id):
    return hue_service.get_automation_state(automation_id)

@router.get("/get_automation_state/")
async def get_automation_state():
    return hue_service.get_automation_state()

@router.get("/stop_automation/{automation_id}")
async def stop_automation(automation_id):
    return hue_service.stop_automation(automation_id)