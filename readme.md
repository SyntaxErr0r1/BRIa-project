# EEG Data Storage and Analysis

The key idea of this project is to store EEG data in a MySQL database and then use it for analysis and visualization using ICA, CCA and extract functional connectivity features.
The project consists of the experimental phase in the JuPyter Notebooks and Application phase which is located in the src/ directory.

## Data Collection

In this project, I used MindRove HeadBand to get eyes closed and eyes open EEG data.
The data is collected in a resting state.

In later stages, pre-recorded data from this work was used:

- M. Torkamani-Azar, S. D. Kanik, S. Aydin and M. Cetin, "Prediction of Reaction Time and Vigilance Variability From Spatio-Spectral Features of Resting-State EEG in a Long Sustained Attention Task," in IEEE Journal of Biomedical and Health Informatics, vol. 24, no. 9, pp. 2550-2558, Sept. 2020, doi: 10.1109/JBHI.2020.2980056. https://ieeexplore.ieee.org/document/9034192 
- (https://github.com/mastaneht/SPIS-Resting-State-Dataset)


## Data Storage

The data is stored in a `MySQL` database. The database is hosted on a remote server (MS Azure). The database is accessed using a Python script via the `sqlalchemy` library. 

The database has 3 tables:

- `Recording` - stores the metadata of the recordings (e.g., sampling rate, recording date, recording duration, etc.)
- `DataChannel` - stores the metadata of the channels (e.g,. channel name, channel number, etc.)
- `Sample` - stores the actual data samples

The DB can be accessed via the implemented Python script `db.py`.

## Data Upload

The data is uploaded to the database using the `upload.py` script. The script takes the following arguments: 

<tt>`upload.py [-h] [-d description] [-n name] [--date DATE] [-c channels] file data_key sampling_rate`</tt>

- `file` - path to the data (`mat`) file
- `data_key` - key of the data in the `mat` file (e.g. `data`)
- `sampling_rate` - sampling rate of the recording
- `--name` - the name of the recording (e.g., `eyes_closed`)
- `--date` - date of the recording (format: `YYYY-MM-DD HH:MM:SS`, default: current date and time)
<!-- - `--recording_duration` - duration of the recording -->
- `--channels` - names of the channels (comma separated) (e.g. `Fp1,Fp2,O1`)

The script parses the data file and uploads the data to the database. The script also creates a new recording and channel entries in the database


## Data Analysis

The data is then downloaded from the database and analyzed using `jupyter` notebooks. The analysis is done in the following steps:
    - Data is downloaded from the database
    - Data is filtered using a bandpass filter
    - Data is segmented into epochs
    - ICA is applied to the data
    - Functional connectivity features are extracted from the data
    - The features are visualized


