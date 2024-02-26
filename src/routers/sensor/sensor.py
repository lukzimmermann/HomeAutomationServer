from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.routers.sensor.sensor_service import get_server_power_data
from src.utils.database import get_db
from src.utils.sensor.sensor_handler import SensorHandler


sensor_handler = SensorHandler()

router = APIRouter(prefix="/sensor", tags=["Sensors"])

@router.get("/getSensors/", tags=["Sensors"])
async def getSensors():
    return str(sensor_handler.sensor_list[0])

@router.get('/getServerPowerData/{value_type}', tags=["Sensors"])
async def getServerPower(value_type, db: Session = Depends(get_db)):
    return get_server_power_data(value_type, db)


