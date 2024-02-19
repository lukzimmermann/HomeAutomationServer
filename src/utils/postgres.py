import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,joinedload
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from models.model import SensorChannelModel, SensorLogModel, SensorModel, Base


engine = create_engine(os.getenv("POSTGRES_CONNECTION"))

metadata = Base.metadata

s1_ch1 = SensorChannelModel(name='Power Channel1', display_name='Power Firewall', unit='W')
s1_ch2 = SensorChannelModel(name='Power Channel2', display_name='Power Server', unit='W')

s2_ch1 = SensorChannelModel(name='Power Channel3', display_name='Power K3s', unit='W')
s2_ch2 = SensorChannelModel(name='Power Channel4', display_name='Power Switch&AccessPoint&Hue', unit='W')

s1 = SensorModel(name='ServerPower1',
                 display_name='ServerPower1',
                 ip_address='10.0.60.10', 
                 mac_address='08:b6:1f:cd:b3:9c',
                 is_active=True,
                 log_interval=10,
                 type='SHELLY_2PM',
                 channels=[s1_ch1, s1_ch2])

s2 = SensorModel(name='ServerPower2',
                 display_name='ServerPower2',
                 ip_address='10.0.60.11', 
                 mac_address='e4:65:b8:46:ba:58',
                 is_active=True,
                 log_interval=10,
                 type='SHELLY_2PM',
                 channels=[s2_ch1, s2_ch2])


s1_ch1_log = SensorLogModel(value=42.3, channel_id=19)


Session = sessionmaker(bind=engine)
session = Session()

session.add(s1_ch1_log)
session.commit()

if False:
    session.add_all([s1, s2])
    session.commit()



sensors = session.query(SensorModel).options(
    joinedload(SensorModel.channels)).all()

session.close()

for sensor in sensors:
    for channel in sensor.channels:
        print(channel)

