import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from src.models.model import SensorModel, SensorLogModel
from src.routers.sensor.shelly import Shelly, Data
from src.utils.singleton import singleton


@singleton
class SensorHandler():
    def __init__(self) -> None:
        self.sensor_list = []
        self.shellys: list[Shelly] = []
        
        self.load_sensors()

    def load_sensors(self) -> list[SensorModel]:
        self. sensor_list = []
        self.shellys = []

        try: 
            engine = create_engine(os.getenv("POSTGRES_CONNECTION"))
            Session = sessionmaker(bind=engine)
            session = Session()
            sensors = session.query(SensorModel).options(joinedload(SensorModel.channels)).all()

            for sensor in sensors:
                if sensor.type == 'SHELLY_2PM':
                    shelly = Shelly(sensor.id, sensor.ip_address, sensor.type)
                    shelly.get_data()
                    self.shellys.append()
        except:
            print("Error: Could not load sensors from db")
        finally:
            session.close()
        self.sensor_list = sensors

        return sensors
    
    def get_sensor_instance(self, id: int) -> Shelly:
        print("getSensorInstance")
        for shelly in self.shellys:
            print(f'ShellyId: {shelly.id}')
            if shelly.id == id:
                return shelly

    def start(self) -> None:
        self.stop()

        for sensor in self.sensor_list:
            if sensor.type == 'SHELLY_2PM':
                #shelly = Shelly(sensor.id, sensor.ip_address, sensor.type)
                shelly = self.get_sensor_instance(sensor.id)
                shelly_listener = self.ShellyListener(self)
                shelly.add_listener(shelly_listener)

                shelly.start_recording(sensor.log_interval, sensor.collection_interval)
            else: print('Fuck off')

    def stop(self) -> None:
        for shelly in self.shellys:
            shelly.stop_recording()
            shelly.listeners = []

    def write_log_to_database(self, log: SensorLogModel) -> None:
        try:
            engine = create_engine(os.getenv("POSTGRES_CONNECTION"))
            Session = sessionmaker(bind=engine)
            session = Session()
            session.add(log)
            session.commit()
        except:
            print("Error: Could not write log to db")
        finally:
            session.close()
    
    class ShellyListener():
        def __init__(self, sensor_handler):
            self.sensor_handler = sensor_handler

        def new_data_available(self, dataset: list[Data]) -> None:
            sensor: SensorModel = self.sensor_handler.get_sensor_by_id(dataset[0].sensor_id)

            if sensor.is_active:
                for channel in sensor.channels:
                    if channel.is_log_value:
                        if ':' in channel.name:
                            channel_index = int(channel.name.split(':')[0])
                            attribute_name = channel.name.split(':')[1]

                        log = SensorLogModel()
                        log.channel_id = channel.id
                        log.value = getattr(dataset[channel_index], attribute_name)

                        self.sensor_handler.write_log_to_database(log)