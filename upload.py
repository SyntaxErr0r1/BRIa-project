from scipy.io import loadmat
import mne
from db import engine, DataChannel, Sample, Recording
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm
import argparse
from datetime import datetime
import sys
from colorama import Fore

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
file = parser.parse_args().file

args = parser.parse_args()


try:
    channels = args.channels.split(',')
    channels = [channel.strip() for channel in channels]
    channels = [element.strip("'") for element in channels]
    channels = [element.strip('"') for element in channels]
except:
    parser.error('Channels must be a comma separated list of strings\n')

print('Channels: ', channels)
exit()

data_EC = loadmat(file)[args.data_key]
data_EC_filter = data_EC['dataRest'][:len(channels), :]

Session = sessionmaker(bind=engine)
session = Session(autoflush=False)

recording = Recording(name="Test recording EC", description="Eyes closed", sampling_rate=2048)
session.add(recording)


for i in tqdm(range(0, data_EC.shape[0])):
    channel_name = channels[i]

    data_channel = DataChannel(channel_name=channel_name, recording=recording)
    session.add(data_channel)
    session.flush()

    data_dicts = []
    for val in data_EC[i]:
        data_dicts.append(dict(value=float(val), data_channel_id=data_channel.id))
    
    session.bulk_insert_mappings(Sample, data_dicts)