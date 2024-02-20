from fastapi import APIRouter
from pydantic import BaseModel

from routers.hue.hue_service import Hue

class Dimm(BaseModel):
    light_id: str
    duration: int
    brightness: int

hue = Hue()

router = APIRouter(prefix="/hue", tags=["Hue Lights"])

@router.get("/getLights/", tags=["Hue Lights"])
async def getLights():
    return hue.get_rooms_from_hue()

@router.put("/setRoom/{room_id}")
async def setRoom(room_id):
    return hue.set_room(room_id)

@router.get("/cinema/")
async def setRoom():
    return hue.cinema_mode()

@router.put("/dimm_light")
async def dimm_light(data: Dimm):
    return hue.dimm_light(data.light_id, data.duration, data.brightness)

@router.get("/get_automation_state/{automation_id}")
async def get_automation_state(automation_id):
    return hue.get_automation_state(automation_id)

@router.get("/get_automation_state/")
async def get_automation_state():
    return hue.get_automation_state()

@router.get("/stop_automation/{automation_id}")
async def stop_automation(automation_id):
    return hue.stop_automation(automation_id)