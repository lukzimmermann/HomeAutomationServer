from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc



from src.routers.sensor.models import ServerPower, Power
from src.utils.sensor.sensor_handler import SensorHandler

sensor_handler = SensorHandler()

def get_server_power_data(value_type: str, session: Session):
    for sensor in sensor_handler.sensor_list:
        if 'serverpower1' in sensor.name.lower():
            router = Power(name = value_type, value = sensor.get_data()[0][value_type].value, unit=sensor.get_data()[0][value_type].unit)
            server = Power(name = value_type, value = sensor.get_data()[1][value_type].value, unit=sensor.get_data()[1][value_type].unit)
        if 'serverpower2' in sensor.name.lower():
            k3s =  Power(name = value_type, value = sensor.get_data()[0][value_type].value, unit=sensor.get_data()[0][value_type].unit)
            switch =  Power(name = value_type, value = sensor.get_data()[1][value_type].value, unit=sensor.get_data()[1][value_type].unit)
    
    return ServerPower(router=router, server=server, k3s=k3s, switch=switch)

            



