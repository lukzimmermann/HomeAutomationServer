from fastapi import APIRouter

from src.routers.hue.hueService import Hue, Room

hue = Hue()

router = APIRouter(prefix="/hue", tags=["Hue Lights"])

@router.get("/getLights/", tags=["Hue Lights"])
async def getLights():
    return hue.get_rooms_from_hue()

@router.put("/setRoom/{room_id}")
async def setRoom(room_id):
    return hue.set_room(room_id)