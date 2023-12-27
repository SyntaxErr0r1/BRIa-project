import json
from flask import Flask, jsonify, request
from copy import deepcopy

import mne
from db import engine, Base, load_recording_async
from sqlalchemy.orm import sessionmaker
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

plt.switch_backend('agg')

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)

modules = [
    {
        'id': 0,
        'name': 'Load data',
        'description': 'This module loads data from MySQL DB',
        'dataId': 1,
        'montageId': 'biosemi64',
        'plotUrl': '/static/0/plot.png',
        'type': 'loadData',
        'dataOutput': [],
        'channelNames': [],
        'statusProcessing': False,
    },
    {
        'id': 1,
        'name': 'High pass filter',
        'description': 'This module applies high pass filter to the data',
        'cutOff': 1,
        'plotUrl': '/static/1/plot.png',
        'type': 'highPassFilter',
        'dataOutput': [],
        'channelNames': [],
        'statusProcessing': False,
    },
    {
        'id': 2,
        'name': 'ICA',
        'description': 'This module applies ICA to the data',
        'componentsPlotUrl': '/static/3/components.png',
        'removedComponents': [1, 2, 3],
        'plotUrl': '/static/2/plot.png',
        'type': 'ica',
        'dataOutput': [],
        'channelNames': [],
        'statusProcessing': False,
    },
]

def stringify_modules(modules):
    mod_copy = deepcopy(modules)
    for module in mod_copy:
        module['dataOutput'] = None
    
    return jsonify(mod_copy)

async def process_module_loadData(data,module) -> bool:
    dataId : int = module['dataId']
    # output data of previous module

    recording = await load_recording_async(session, dataId, tqdm)

    data = np.array(recording['data'])
    channel_names = recording['channels']


    eeg_EC = data * 1e-6 # convert to volts

    # create info object
    info = mne.create_info(
        ch_names=channel_names,
        ch_types=['eeg']*len(channel_names),
        sfreq=256)

    # create raw object
    raw = mne.io.RawArray(eeg_EC, info)

    print("DATA SHAPE",data.shape)

    montage = mne.channels.make_standard_montage(module['montageId'])
    
    # Afz will not be part of ICA
    raw.set_channel_types({'Afz': 'misc'})
    raw.set_montage(montage)

    module['dataOutput'] = raw
    module['channelNames'] = channel_names

    # save plot to static/0/plot.png
    fig = raw.plot( title="Before", scalings='auto');
    fig.savefig('./static/0/plot.png')

    return module

async def process_module_highPassFilter(data,module) -> bool:
    # output data of previous module
    module['dataOutput'] = data

    print("DATA TYPE",type(data))

    print("DATA SHAPE",len(data))

    # save plot to static/1/plot.png
    fig = data.plot( title="Before", scalings='auto');
    fig.savefig('./static/1/plot.png')

    return module

def process_modules():
    for module in modules:
        process_module(module['id'])

@app.route('/modules/<int:module_id>', methods=['PUT'])
def update_module(module_id):
    module = request.get_json()
    modules[module_id - 1] = module
    return stringify_modules(module)

@app.route('/modules/<int:module_id>/process', methods=['POST'])
async def process_module(module_id):

    if module_id >= 1:
        data = deepcopy(modules[module_id - 1]['dataOutput'])
    else:
        data = None

    
    module = modules[module_id]
    module['statusProcessing'] = True

    if module['type'] == 'loadData':
        result = await process_module_loadData(data,module)
    elif module['type'] == 'highPassFilter':
        result = await process_module_highPassFilter(data,module)
    elif module['type'] == 'ica':
        pass

    result['statusProcessing'] = False
    modules[module_id] = result

    return stringify_modules(modules)

@app.route('/modules/<int:module_id>', methods=['GET'])
def get_module(module_id):
    return stringify_modules(modules[module_id - 1])

@app.route('/modules', methods=['GET'])
def get_modules():
    return stringify_modules(modules)

@app.route('/modules', methods=['POST'])
def set_modules():
    modules = request.get_json()
    print(modules)
    return stringify_modules(modules)


if __name__ == '__main__':
   app.run(port=8888, debug=True)