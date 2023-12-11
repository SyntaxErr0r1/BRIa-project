from db import Recording, DataChannel, Sample, engine, meta, Base
from sqlalchemy.orm import sessionmaker
from typing import List

# create session
Session = sessionmaker(bind=engine)
session = Session()

# get all recordings
recordings = session.query(Recording).all()

for recording in recordings:
    print(recording.name, recording.id)


def load_recoding(id: int) -> (List[str],List[int]):
    """Function that loads the recorging from DB and returns channel info and data"""
    # get recording
    recording = session.query(Recording).filter_by(id=id).first()

    # get all data channels
    data_channels = session.query(DataChannel).filter_by(recording_id=id).all()

    # get channel names
    channel_names = []
    for data_channel in data_channels:
        channel_names.append(data_channel.channel_name)

    # get channel data
    all_channels_data = []
    for data_channel in data_channels:
        channel_data = []

        for sample in data_channel.samples:
            channel_data.append(sample.value)
        all_channels_data.append(channel_data)

    return channel_names, all_channels_data

# load recording 1
channel_names, all_channels_data = load_recoding(1)

print(channel_names)


# print first 10 FP1 samples
print(all_channels_data[0][0:10])


# close session
session.close()


