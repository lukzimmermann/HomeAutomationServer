import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from typing import List
from src.models.model import SensorModel

from src.utils.sensor.sensor import Sensor, SensorType
from src.utils.sensor.shelly import Shelly
from src.utils.singleton import singleton


@singleton
class SensorHandler():
    def __init__(self) -> None:
        self.sensor_list = self.initialize_sensors()

    def initialize_sensors(self) -> list[Sensor]:
        new_sensors: list[Sensor] = []
        try: 
            engine = create_engine(os.getenv("POSTGRES_CONNECTION"))
            Session = sessionmaker(bind=engine)
            session = Session()
            sensors = session.query(SensorModel).options(joinedload(SensorModel.channels)).all()

            for sensor in sensors:
                if sensor.type == SensorType.SHELLY_2PM.value:
                    shelly = Shelly(sensor.id, sensor.name, sensor.ip_address)
                    new_sensors.append(shelly)
        except Exception as e:
            print(f"Error: Could not load sensors from db. {e}")
        finally:
            session.close()

        return new_sensors

    def start(self) -> None:
        self.stop()

        for sensor in self.sensor_list:
            sensor_instance = self.get_sensor_instance(sensor.id)
            shelly_listener = self.ShellyListener(self)
            sensor_instance.add_listener(shelly_listener)
            sensor_instance.start_recording(sensor.log_interval, sensor.collection_interval)

    def stop(self) -> None:
        for sensor in self.sensor_list:
            sensor.stop_recording()
            sensor.listeners = []

        
