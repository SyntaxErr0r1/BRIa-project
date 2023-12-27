# Author: Juraj Dedič, xdedic07
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
from typing import List, Tuple
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
    channel_name = Column(String(16))

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


def load_recoding(session, id: int, pbar_provider) -> tuple[List[str],List[int]]:
    """Function that loads the recorging from DB and returns channel info and data.
    
Arguments: session {sqlalchemy.orm.session.Session} -- DB session
id {int} -- ID of the recording to load
pbar_provider {function} -- function that returns a progress bar object (e.g. tqdm)"""
    
    # get recording
    recording = session.query(Recording).filter_by(id=id).first()

    # get all data channels
    data_channels = session.query(DataChannel).filter_by(recording_id=id).all()

    # get channel names
    channel_names = []
    for data_channel in data_channels:
        channel_names.append(data_channel.channel_name)

    if pbar_provider is not None:
        pbar = pbar_provider(data_channels, desc='Loading channel data from DB', unit='channel')
    else:
        pbar = data_channels
    # get channel data
    all_channels_data = []
    for data_channel in pbar:
        channel_data = []

        for sample in data_channel.samples:
            channel_data.append(sample.value)
        all_channels_data.append(channel_data)

    return channel_names, all_channels_data


async def load_recording_async(session, id: int, pbar_provider) -> dict:
    """Function that loads the recorging from DB and returns channel info and data.
    
Arguments: session {sqlalchemy.orm.session.Session} -- DB session
id {int} -- ID of the recording to load
pbar_provider {function} -- function that returns a progress bar object (e.g. tqdm)"""
    
    # get recording
    recording = session.query(Recording).filter_by(id=id).first()

    # get all data channels
    data_channels = session.query(DataChannel).filter_by(recording_id=id).all()

    # get channel names
    channel_names = []
    for data_channel in data_channels:
        channel_names.append(data_channel.channel_name)

    if pbar_provider is not None:
        pbar = pbar_provider(data_channels, desc='Loading channel data from DB', unit='channel')
    else:
        pbar = data_channels
    # get channel data
    all_channels_data = []
    for data_channel in pbar:
        channel_data = []

        for sample in data_channel.samples:
            channel_data.append(sample.value)
        all_channels_data.append(channel_data)

    return {
        'channels':channel_names,
        'data': all_channels_data
    }

