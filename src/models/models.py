import datetime

from sqlalchemy import Boolean, Integer, String, Column, ForeignKey, Float, Date
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()



class SensorModel(Base):
    __tablename__ = 'sensor'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    display_name = Column(String)
    ip_address = Column(String, nullable=False)
    mac_address = Column(String, nullable=False)
    creation_data = Column(Date, nullable=False, default=datetime.datetime.now())
    log_interval = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
