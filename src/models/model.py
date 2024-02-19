import datetime
from sqlalchemy import Boolean, Integer, String, Column, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class SensorModel(Base):
    __tablename__ = 'sensor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    display_name = Column(String)
    ip_address = Column(String, nullable=False, unique=True)
    mac_address = Column(String, nullable=False, unique=True)
    creation_data = Column(DateTime, nullable=False, default=datetime.datetime.utcnow())
    is_active = Column(Boolean, nullable=False, default=False)
    log_interval = Column(Integer, nullable=False, default=600)
    collection_interval = Column(Integer, nullable=False, default=10)
    type = Column(String, nullable=False)
    channels = relationship('SensorChannelModel', backref='channel')

    def __repr__(self):
        return f'Id: {self.id}, {self.name}, {self.display_name}, {self.ip_address}'


class SensorChannelModel(Base):
    __tablename__ = 'sensor_channel'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_id = Column(Integer, ForeignKey(SensorModel.id, ondelete='CASCADE'), nullable=False)
    name = Column(String, nullable=False)
    display_name = Column(String)
    description = Column(String)
    unit = Column(String, nullable=False)
    logs = relationship('SensorLogModel', backref='logs')

    def __repr__(self):
        return f'Id: {self.id}, Name: {self.name}, DisplayName: {self.display_name}, Unit: {self.unit}'


class SensorLogModel(Base):
    __tablename__ = 'sensor_log'
    entry_date = Column(DateTime, primary_key=True, default=datetime.datetime.now())
    channel_id = Column(Integer, ForeignKey(SensorChannelModel.id, ondelete='CASCADE'), nullable=False)
    value = Column(Float, nullable=False)