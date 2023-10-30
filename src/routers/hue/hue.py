from fastapi import APIRouter

from src.routers.hue.hueService import Hue, Room

hue = Hue()

router = APIRouter(prefix="/hue", tags=["Hue Lights"])

@router.get("/getLights/", tags=["Hue Lights"])
async def getLights():
    return hue.get_rooms_from_hue()

