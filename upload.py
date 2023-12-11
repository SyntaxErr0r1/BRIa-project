from scipy.io import loadmat
import mne
from db import engine, DataChannel, Sample, Recording
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm
import argparse
from datetime import datetime
import sys
from colorama import Fore, Back, Style
import logging
from logging import error, warning, info, debug

loger = logging.getLogger(__name__)
logFormatter = logging.Formatter(fmt='['+Style.BRIGHT+'%(levelname)s'+Style.RESET_ALL+'] %(message)s')

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
loger.addHandler(consoleHandler)
loger.setLevel(logging.DEBUG)


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(Fore.RED+'Error: '+Fore.RESET+'%s\n' % message)
        self.print_help()
        sys.exit(2)

parser = MyParser(
                    prog='upload.py',
                    description='Upload EEG data to MySQL database',
                    epilog='')

parser.add_argument('file', metavar='file', type=str, help='Path to the mat file')
parser.add_argument('data_key', metavar='data_key', type=str, help='Key of the data in the mat file')
parser.add_argument('samplig_rate', metavar='sampling_rate', type=int, help='Sampling rate of the EEG data')
parser.add_argument('-d', '--description', metavar='description', type=str)
parser.add_argument('-n', '--name', metavar='name', type=str)
parser.add_argument(
        '--date',
        type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S'),
        default=datetime.now(),
)
parser.add_argument('-c', '--channels', metavar='channels', type=str)

args = parser.parse_args()

file = args.file
data_key = args.data_key
print('Data key: ', data_key)

try:
    channels = args.channels.split(',')
    channels = [channel.strip() for channel in channels]
    channels = [element.strip("'") for element in channels]
    channels = [element.strip('"') for element in channels]
except:
    parser.error('Channels must be a comma separated list of strings\n')


data_EC = loadmat(file)[args.data_key]

if(len(channels) > len(data_EC)):
    loger.error('Too many channels specified ('+str(len(channels))+'). Dataset has only '+str(len(data_EC))+' channels')
elif(len(channels) < len(data_EC)):
    loger.warning('Specified only '+str(len(channels))+', but the dataset has '+str(len(data_EC))+' channels (will be truncated)')

data_EC_filter = data_EC[:len(channels), :]

Session = sessionmaker(bind=engine)
session = Session(autoflush=False)

recording = Recording(name="Test recording EC", description="Eyes closed", sampling_rate=2048)
session.add(recording)


for i in tqdm(range(0, len(channels)), desc='Uploading channel data to DB', unit='channel'):
    channel_name = channels[i]

    data_channel = DataChannel(channel_name=channel_name, recording=recording)
    session.add(data_channel)
    session.flush()

    data_dicts = []
    for val in data_EC[i]:
        data_dicts.append(dict(value=float(val), data_channel_id=data_channel.id))
    
    session.bulk_insert_mappings(Sample, data_dicts)

logging.info('Commiting changes to DB...')
session.commit()