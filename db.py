# Experiment class sqlalchemy model

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.types import ARRAY
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import func
import sqlalchemy
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv
import os
load_dotenv()

MYSQL_USERNAME : str = os.getenv("MYSQL_USERNAME")
MYSQL_HOSTNAME : str = os.getenv("MYSQL_HOSTNAME")
MYSQL_PASSWORD : str = os.getenv("MYSQL_PASSWORD")

# create engine
connection_str = "mysql+mysqlconnector://"+MYSQL_USERNAME+":"+MYSQL_PASSWORD+"@"+MYSQL_HOSTNAME+"/eeg"

engine = sqlalchemy.create_engine(connection_str)

if not database_exists(engine.url):
    create_database(engine.url)


# get db meta
meta = sqlalchemy.MetaData()

# get all tables
print(meta.tables.keys())


Base = declarative_base()

class Recording(Base):
    __tablename__ = 'recording'
    id = mapped_column(Integer, primary_key=True)
    
    name = Column(String(255))
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    # sampling rate
    sampling_rate = Column(Integer)

    # duration in seconds
    duration = Column(Float, nullable=True)

    # one to many relationship with data channel
    data_channels = relationship("DataChannel", back_populates="recording")

class DataChannel(Base):
    __tablename__ = 'data_channel'
    id = mapped_column(Integer, primary_key=True)
    channel_name = Column(String(16), unique=True)

    #many to one relationship with recording
    recording_id = mapped_column(Integer, ForeignKey('recording.id'))
    recording = relationship("Recording", back_populates="data_channels")

    # one to many relationship with data
    samples = relationship("Sample", back_populates="data_channel")
    

class Sample(Base):
    __tablename__ = 'sample'
    id = mapped_column(Integer, primary_key=True)
    
    value = Column(Float)

    # many to one relationship with data channel
    data_channel_id = mapped_column(Integer, ForeignKey('data_channel.id'))
    data_channel = relationship("DataChannel", back_populates="samples")


Base.metadata.create_all(engine)