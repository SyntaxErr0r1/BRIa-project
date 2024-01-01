import json
from flask import Flask, jsonify, request
from copy import deepcopy
from scipy.io import loadmat
import mne
from db import engine, Base, load_recording_async, Recording, DataChannel, Sample
from sqlalchemy.orm import sessionmaker
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
from io import BufferedReader, BytesIO
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
from mne_connectivity import spectral_connectivity_epochs
from mne.datasets import sample
# from mne_connectivity.viz import plot_sensors_connectivity
from connectivity import plot_sensors_connectivity
# from mayavi import mlab
import pyvista as pv

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'mat'}

pv.set_jupyter_backend(None)
plt.switch_backend('agg')

Session = sessionmaker(bind=engine)

app = Flask(__name__)

modules = [
    {
        'id': 0,
        'name': 'Load data',
        'description': 'This module loads data from MySQL DB',
        'dataId': 1,
        'montageId': 'biosemi64',
        'plotUrl': '/static/0/plot.png',
        'scalings': 'auto',
        'plotDuration': 3,
        'type': 'loadData',
        'dataOutput': None,
        'channelNames': [],
        'statusProcessing': False,
    },
    {
        'id': 1,
        'name': 'High pass filter',
        'description': 'This module applies high pass filter to the data',
        'cutOff': 1,
        'plotUrl': '/static/1/plot.png',
        'scalings': 0.00000003,
        'plotDuration': 3,
        'type': 'highPassFilter',
        'dataOutput': None,
        'channelNames': [],
        'statusProcessing': False,
    },
    {
        'id': 2,
        'name': 'ICA',
        'description': 'This module applies ICA to the data',
        'componentsPlotUrl': '/static/2/components.png',
        'removedComponents': [0,1,2,9,10,17],
        'plotUrl': '/static/2/plot.png',
        'scalings': 0.00000003,
        'plotDuration': 3,
        'type': 'ica',
        'dataOutput': None,
        'channelNames': [],
        'statusProcessing': False,
    },
    {
        'id': 3,
        'name': 'Connectivity',
        'description': 'This module calculates connectivity',
        'plotConnectivity': '/static/2/plotConnectivity.png',
        'scalings': 0.00000003,
        'plotDuration': 3,
        'type': 'connectivity',
        'dataOutput': None,
        'channelNames': [],
        'statusProcessing': False,
    },
]

def get_scalings(module):
    scalings = 'auto'
    try:
        if type(module['scalings']) == str:
            scalings = module['scalings']
        elif type(module['scalings']) == float:
            scalings = dict(eeg=module['scalings'])
    except:
        pass
    return scalings

def create_dir_structure():
    """Creates directory structure for storing static files"""
    try:
        os.makedirs('./static')
    except:
        pass

    try:
        os.makedirs('./uploads')
    except:
        pass

    for module in modules:
        try:
            os.makedirs('./static/'+str(module['id']))
        except:
            pass

def stringify_modules(modules):
    """Converts modules to JSON string
    :param modules: list of modules or single module"""

    def stringify_module(module):
        module['dataOutput'] = None
        return module

    mod_copy = deepcopy(modules)
    if isinstance(mod_copy, list):
        for module in mod_copy:
            stringify_module(module)
    elif isinstance(mod_copy, dict):
        stringify_module(mod_copy)
    
    return jsonify(mod_copy)

async def process_module_loadData(data, module) -> bool:
    session = Session()
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
    scalings = get_scalings(module)
    fig = raw.plot( title="Before", scalings=scalings, duration=module['plotDuration']);
    fig.savefig('./static/0/plot.png')

    return module

async def process_module_highPassFilter(data,module) -> bool:
    # output data of previous module

    data = data.filter(l_freq=module['cutOff'], h_freq=None)
    
    scalings = get_scalings(module)

    # save plot to static/1/plot.png
    fig = data.plot( title="Before", scalings=scalings, duration=module['plotDuration']);
    fig.savefig('./static/1/plot.png')

    module['dataOutput'] = data

    return module

async def process_module_ica(data,module) -> bool:
    # output data of previous module
    raw_tmp = data
    raw_tmp.filter(l_freq=1, h_freq=None)
    ica = mne.preprocessing.ICA(method="picard") 
    fit_params={"extended": True}
    random_state=1
    ica.fit(raw_tmp)

    fig = ica.plot_components(inst=raw_tmp, picks=range(25));
    try:
        fig.savefig('./static/2/components.png')
    except:
        print("Error saving components plot")


    ica.exclude = module['removedComponents']
    raw_corrected = raw_tmp

    scalings = get_scalings(module)

    ica.apply(raw_corrected)
    fig = raw_corrected.plot(n_channels=32, title="After", scalings=scalings, duration=module['plotDuration']);
    fig.savefig('./static/2/plot.png')

    module['dataOutput'] = raw_corrected

    return module

def process_module_connectivity(data,module) -> bool:
    raw_corrected = data
    epochs = mne.make_fixed_length_epochs(raw=raw_corrected, duration=0.5, overlap=0.25)
    times = epochs.times
    ch_names = epochs.ch_names


    # Pick MEG gradiometers
    picks = mne.pick_types(
        raw_corrected.info, meg=False, eeg=True, stim=False, eog=False
    )

    # Compute connectivity for band containing the evoked response.
    # We exclude the baseline period:
    fmin, fmax = 4.0, 9.0
    sfreq = raw_corrected.info["sfreq"]  # the sampling frequency
    tmin = 0.0  # exclude the baseline period
    epochs.load_data().pick_types(eeg=True)
    con = spectral_connectivity_epochs(
        epochs,
        method="pli",
        mode="multitaper",
        sfreq=sfreq,
        fmin=fmin,
        fmax=fmax,
        faverage=True,
        tmin=tmin,
        mt_adaptive=False,
        n_jobs=1,
    )

    # Now, visualize the connectivity in 3D:
    fig = plot_sensors_connectivity(epochs.info, con.get_data(output="dense")[:, :, 0]);
    # close the figure to avoid showing it
    # pv.close_all()
    # fig.scene.save('./static/3/plotConnectivity.png')
    # fig.savefig('./static/3/plotConnectivity.png')
    print(str(fig))

    # output data of previous module
    return module

def process_modules():
    for module in modules:
        process_module(module['id'])

@app.route('/modules/<int:module_id>/', methods=['POST'])
def update_module(module_id):
    module = request.get_json()

    # set all keys of module to the new values (except id and dataOutput)
    for key in module:
        if key != 'id' and key != 'dataOutput' and key != 'statusProcessing':
            modules[module_id][key] = module[key]
    # modules[module_id] = module
    return stringify_modules(module)

def get_latest_data(module_id):
    """Returns the data output of the previous module
    If the previous module data does not have data yet, it will get the data from the module before that"""
    if module_id >= 1:
        previous_module_data = modules[module_id - 1]['dataOutput']
        if previous_module_data is not None:
            return deepcopy(previous_module_data)
        else:
            return get_latest_data(module_id - 1)
    else:
        return None
    
@app.route('/data/', methods=['GET'])
@app.route('/data', methods=['GET'])
def get_data():
    modules_data = ""
    for module in modules:
        if module['dataOutput'] is None:
            modules_data += str(module["id"])+" None" + "\n"
        else:
            modules_data += str(module["id"])+" "+str(len(module["dataOutput"])) + "\n"

    return modules_data

@app.route('/modules/<int:module_id>/process/', methods=['POST'])
async def process_module(module_id):

    # if module_id >= 1:
    #     data = deepcopy(modules[module_id - 1]['dataOutput'])
    # else:
    #     data = None

    data = get_latest_data(module_id)
    
    module = modules[module_id]
    module['statusProcessing'] = True

    if module['type'] == 'loadData':
        result = await process_module_loadData(data,module)
    elif module['type'] == 'highPassFilter':
        result = await process_module_highPassFilter(data,module)
    elif module['type'] == 'ica':
        result = await process_module_ica(data,module)
    elif module['type'] == 'connectivity':
        result = process_module_connectivity(data,module)

    result['statusProcessing'] = False
    modules[module_id] = result

    return stringify_modules(modules)

@app.route('/modules/<int:module_id>', methods=['GET'])
@app.route('/modules/<int:module_id>/', methods=['GET'])
def get_module(module_id):
    return stringify_modules(modules[module_id])

@app.route('/modules', methods=['GET'])
@app.route('/modules/', methods=['GET'])
def get_modules():
    return stringify_modules(modules)

@app.route('/modules', methods=['POST'])
@app.route('/modules/', methods=['POST'])
def set_modules():
    modules = request.get_json()
    print(modules)
    return stringify_modules(modules)

@app.route('/recordings', methods=['GET'])
@app.route('/recordings/', methods=['GET'])
def get_recordings():
    session = Session()
    recordings = session.query(Recording).all()
    recordings = [recording.to_dict() for recording in recordings]
    return jsonify(recordings)

@app.route('/recordings/<int:recording_id>', methods=['DELETE'])
def delete_recording(recording_id):
    session = Session()

    print("Deleting recording",recording_id)

    # delete all samples and data channels of the recording
    session.query(Sample).filter(Sample.data_channel.has(recording_id=recording_id)).delete(synchronize_session=False)
    session.query(DataChannel).filter(DataChannel.recording_id==recording_id).delete(synchronize_session=False)
    session.query(Recording).filter(Recording.id==recording_id).delete(synchronize_session=False)

    session.commit()
    return jsonify({'success': True}) 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_channels(channels) -> list | None:
    try:
        channels = channels.split(',')
        channels = [channel.strip() for channel in channels]
        channels = [element.strip("'") for element in channels]
        channels = [element.strip('"') for element in channels]
        return channels
    except:
        return None

@app.route('/recordings/', methods=['POST'])
def upload_file():

    warning = None
    error = None

    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return jsonify({'success': False, 'error': 'No file part', 'warning': warning})
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return jsonify({'success': False, 'error': 'No selected file', 'warning': warning})
    if file and allowed_file(file.filename):
        # filename = secure_filename(file.filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
        print("form",request.form)
        data_key = request.form['data_key']
        name = request.form['name']
        description = request.form['description']
        sampling_rate = request.form['sampling_rate']

        file.seek(0)
        file_contents = file.read()
        print("File contents",len(file_contents))

        bytes_io = BytesIO(file_contents)
        
        bytes_io.seek(0)
        data = loadmat(bytes_io)[data_key]
        print("Data length",len(data))

        channels = parse_channels(request.form['channels'])

        if(len(channels) > len(data)):
            return jsonify({'success': False, 'error': 'Too many channels specified ('+str(len(channels))+'). Dataset has only '+str(len(data))+' channels'})
        elif(len(channels) < len(data)):
            warning = ('Specified only '+str(len(channels))+', but the dataset has '+str(len(data))+' channels (will be truncated)')

        session = Session(autoflush=False)

        recording = Recording(name=name, description=description, sampling_rate=sampling_rate, created_at=None)
        session.add(recording)


        for i in tqdm(range(0, len(channels)), desc='Uploading channel data to DB', unit='channel'):
            channel_name = channels[i]

            data_channel = DataChannel(channel_name=channel_name, recording=recording)
            session.add(data_channel)
            session.flush()

            data_dicts = []
            for val in data[i]:
                data_dicts.append(dict(value=float(val), data_channel_id=data_channel.id))
            
            session.bulk_insert_mappings(Sample, data_dicts)

        print('Commiting changes to DB...')
        session.commit()


        return jsonify({'success': True, 'warning': warning, 'error': error})

    return jsonify({'success': False, 'error': 'Unknown error', 'warning': warning})


if __name__ == '__main__':
    create_dir_structure()
    app.url_map.strict_slashes = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run(port=8888, debug=True)