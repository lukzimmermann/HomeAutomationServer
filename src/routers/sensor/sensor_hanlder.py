import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker





engine = create_engine(os.getenv("POSTGRES_CONNECTION"))

metadata = Model.Base.metadata


Session = sessionmaker(bind=engine)
session = Session()
#
#sensor = SensorModel(name='ServerPower2', 
#                     ip_address='10.0.60.11', 
#                     mac_address='e4:65:b8:46:ba:58',
#                     is_active=True,
#                     log_interval=10,
#                     type='SHELLY_2PM')
#
#session.add(sensor)
#session.commit()


sensors = session.query(SensorModel).all()

for sensor in sensors:
    print(sensor)





