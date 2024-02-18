import datetime
from sqlalchemy import Boolean, Integer, String, Column, ForeignKey, Float, Date
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class SensorModel(Base):
    __tablename__ = 'sensor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    display_name = Column(String)
    ip_address = Column(String, nullable=False)
    mac_address = Column(String, nullable=False)
    creation_data = Column(Date, nullable=False, default=datetime.datetime.now())
    is_active = Column(Boolean, nullable=False, default=False)
    log_interval = Column(Integer, nullable=False, default=600)
    type = Column(String, nullable=False)
    channels = relationship('SensorChannelModel', backref='channel')

    def __repr__(self):
        return self.name


class SensorChannelModel(Base):
    __tablename__ = 'sensor_channel'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_id = Column(Integer, ForeignKey(SensorModel.id, ondelete='CASCADE'), nullable=False)
    name = Column(String, nullable=False)
    display_name = Column(String)
    description = Column(String)
    unit = Column(String, nullable=False)
    logs = relationship('SensorLogModel', backref='logs')


class SensorLogModel(Base):
    __tablename__ = 'sensor_log'
    entry_date = Column(Date, primary_key=True, default=datetime.datetime.now())
    channel_id = Column(Integer, ForeignKey(SensorChannelModel.id, ondelete='CASCADE'), nullable=False)
    value = Column(Float, nullable=False)