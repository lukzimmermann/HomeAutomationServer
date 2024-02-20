import os
import sys
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload

from shelly import Data, Shelly

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(parent_dir)

from models.model import SensorLogModel, SensorModel





class SensorHandler():
    def __init__(self) -> None:
        self.sensor_list = []
        self.shellys: list[Shelly] = []
        
        self.load_sensors()

        self.start()

        time.sleep(300)

        self.stop()

    def load_sensors(self) -> list[SensorModel]:
        self. sensor_list = []

        try:
            engine = create_engine(os.getenv("POSTGRES_CONNECTION"))
            Session = sessionmaker(bind=engine)
            session = Session()
            sensors = session.query(SensorModel).options(joinedload(SensorModel.channels)).all()
        except:
            print("Error: Could not load sensors from db")
        finally:
            session.close()
        self.sensor_list = sensors

        return sensors
    
    def get_sensor_by_id(self, id: int) -> SensorModel:
        for sensor in self.sensor_list:
            if sensor.id == id:
                return sensor
        
        return None

    def start(self):
        self.stop()

        for sensor in self.sensor_list:
            if sensor.type == 'SHELLY_2PM':
                print(sensor)
                shelly = Shelly(sensor.id, sensor.ip_address, sensor.type)
                
                shelly_listener = self.ShellyListener(self)
                shelly.add_listener(shelly_listener)
                self.shellys.append(shelly)

                shelly.start_recording(sensor.log_interval, sensor.collection_interval)
            else: print('Fuck off')

    def stop(self):
        for shelly in self.shellys:
            shelly.stop_recording()
            shelly.listeners = []
    
    class ShellyListener():
        def __init__(self, sensor_handler):
            self.sensor_handler = sensor_handler

        def new_data_available(self, dataset: list[Data]):
            # Accessing get_sensor_by_id through the outer class instance
            sensor: SensorModel = self.sensor_handler.get_sensor_by_id(dataset[0].sensor_id)

            for channel in sensor.channels:
                if ':' in channel.name:
                    channel_index = int(channel.name.split(':')[0])
                    attribute_name = channel.name.split(':')[1]

                log = SensorLogModel()
                log.channel_id = channel.id
                log.value = getattr(dataset[channel_index], attribute_name)

                print(f'{channel.display_name}: {log.value}{channel.unit}')
            print()