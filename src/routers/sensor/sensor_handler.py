import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(parent_dir)

from models.model import Base, SensorModel


class SensorHandler():
    def __init__(self) -> None:
        self.sensor_list = self.load_sensors()


    def load_sensors(self) -> list[SensorModel]:
        try:
            engine = create_engine(os.getenv("POSTGRES_CONNECTION"))
            Session = sessionmaker(bind=engine)
            session = Session()
            sensors = session.query(SensorModel).options(joinedload(SensorModel.channels)).all()
        except:
            print("Error: Could not load sensors from db")
        finally:
            session.close()

        return sensors