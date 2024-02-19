import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.model import Base, SensorChannelModel, SensorModel



engine = create_engine(os.getenv("POSTGRES_CONNECTION"))

metadata = Base.metadata


Session = sessionmaker(bind=engine)
session = Session()


channel1 = SensorChannelModel(name='Channel1', display_name='Firewall', unit='W')
channel2 = SensorChannelModel(name='Channel2', display_name='Server', unit='W')

sensor = SensorModel(name='ServerPower2', 
                     ip_address='10.0.60.11', 
                     mac_address='e4:65:b8:46:ba:58',
                     is_active=True,
                     log_interval=10,
                     type='SHELLY_2PM',
                     channels=[channel1, channel2])

session.add(sensor)
session.commit()

sensors = session.query(SensorModel).all()

for sensor in sensors:
    print(sensor)

#session.delete(sensors[0])
#session.commit()